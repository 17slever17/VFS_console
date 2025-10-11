import xml.etree.ElementTree as ET
import os

from ui import print_output, root
from vfs import VFS, VFSNode, state


def run_command_line(cmd_line):
    print_output(cmd_line)
    if not cmd_line.strip():
        return

    parts = cmd_line.strip().split(maxsplit=1)
    cmd = parts[0]
    args = parts[1].strip() if len(parts) > 1 else []

    if cmd == "vfs-save":
        if not args:
            print_output("vfs-save: specify path to save XML")
            return
        try:
            save_vfs_to_xml(state.vfs, args)
            print_output(f"VFS saved to {args}")
        except Exception as e:
            print_output(f"Error saving VFS: {e}")
        return

    if cmd == "ls":
        if args:
            args = args.split()
            print_output(f"ls args: {' '.join(args)}")
        else:
            print_output("ls: no args")

    elif cmd == "cd":
        if not args:
            return
        elif " " in args and not (args.startswith('"') and args.endswith('"')):
            print_output("cd: too many arguments")
        else:
            if not args:
                return
            elif args.startswith('"') and args.endswith('"'):
                args_list = args[1:-1].strip().split('/')
            else:
                args_list = args.split('/')
            if args_list:
                if args_list[0] in ["", ".", ".."] and len(args) > 1 and args_list[1] == "":
                    args_list.pop()
                if args_list[0] == "":
                    state.dir_stack.clear()
                elif args_list[0] == ".." and state.dir_stack:
                    state.dir_stack.pop()
                for arg in args_list[1:]:
                    state.dir_stack.append(arg)

    elif cmd == "exit":
        root.destroy()

    else:
        print_output(f"Unknown command: {cmd}")


def load_vfs_from_xml(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"VFS file not found: {file_path}")
    try:
        tree = ET.parse(file_path)
        root_elem = tree.getroot()
    except ET.ParseError:
        raise ValueError(f"Invalid XML format in VFS file: {file_path}")

    vfs = VFS()

    def parse_node(elem, parent_node):
        for child in elem:
            name = child.attrib.get("name")
            type_ = child.tag
            if type_ == "dir":
                node = VFSNode(name, is_dir=True)
                parent_node.children[name] = node
                parse_node(child, node)
            elif type_ == "file":
                content = child.text or ""
                node = VFSNode(name, is_dir=False, content=content)
                parent_node.children[name] = node

    parse_node(root_elem, vfs.root)
    state.vfs = vfs


def save_vfs_to_xml(vfs, file_path):
    root_elem = ET.Element("vfs")

    def node_to_elem(node):
        if node.is_dir:
            elem = ET.Element("dir", name=node.name)
            for child in node.children.values():
                elem.append(node_to_elem(child))
        else:
            elem = ET.Element("file", name=node.name, encoding="text")
            elem.text = node.content
        return elem

    for child in vfs.root.children.values():
        root_elem.append(node_to_elem(child))

    tree = ET.ElementTree(root_elem)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
