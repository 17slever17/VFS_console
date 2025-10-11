import os
import argparse
import tkinter as tk
from ui import root, entry, print_output, prompt
from commands import run_command_line
from script_runner import execute_start_script
import xml.etree.ElementTree as ET
from vfs import VFS, VFSNode, state


def run_command(event=None):
    cmd_line = entry.get()
    entry.delete(0, tk.END)
    run_command_line(cmd_line)
    prompt()


def parse_and_start():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--vfs-root", help="Path to physical VFS root", default=None)
    parser.add_argument(
        "--start-script", help="Path to start script", default=None)
    args = parser.parse_args()

    state.vfs = VFS()

    print_output(
        "VFS Emulator (prototype)\nCommands: ls, cd, exit, vfs-save\n")
    print_output(f"Debug: --vfs-root = {args.vfs_root}")
    print_output(f"Debug: --start-script = {args.start_script}\n")

    if args.vfs_root:
        try:
            load_vfs_from_xml(args.vfs_root)
            print_output(f"VFS loaded from {args.vfs_root}")
        except Exception as e:
            print_output(f"Error loading VFS: {e}")

    if args.start_script:
        state.start_script = args.start_script
        execute_start_script(state.start_script)

    prompt()


def load_vfs_from_xml(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"VFS file not found: {file_path}")
    try:
        tree = ET.parse(file_path)
        root_elem = tree.getroot()
    except ET.ParseError:
        raise ValueError(f"Invalid XML format in VFS file: {file_path}")

    vfs = state.vfs

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


if __name__ == "__main__":
    entry.bind("<Return>", run_command)
    parse_and_start()
    root.mainloop()
