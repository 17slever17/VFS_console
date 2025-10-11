import xml.etree.ElementTree as ET

from ui import print_output, root
from vfs import state


def run_command_line(cmd_line):
    print_output(cmd_line)
    if not cmd_line.strip():
        return

    parts = cmd_line.strip().split(maxsplit=1)
    cmd = parts[0]
    args = parts[1].strip() if len(parts) > 1 else None

    COMMANDS = {
        "vfs-save": save_vfs_to_xml,
        "ls": ls_command,
        "cd": cd_command,
        "rev": rev_command,
        "uniq": uniq_command,
        "wc": wc_command,
        "exit": exit_command
    }

    func = COMMANDS.get(cmd)
    if func:
        if cmd == "exit":
            func()
        else:
            func(args)
    else:
        print_output(f"Unknown command: {cmd}")


def save_vfs_to_xml(file_path=None):
    """
    Сохраняет текущее состояние VFS (state.vfs) в XML
    """
    if not file_path:
        print_output("vfs-save: specify path to save XML")
        return

    try:
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

        # добавляем всех детей корня VFS
        for child in state.vfs.root.children.values():
            root_elem.append(node_to_elem(child))

        tree = ET.ElementTree(root_elem)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print_output(f"VFS saved to {file_path}")

    except Exception as e:
        print_output(f"Error saving VFS: {e}")


def split_path(path):
    """
    Разбивает путь "/a/b/c" на компоненты
    """
    parts = [p for p in path.split('/') if p != ""]
    return parts


def normalize_path(path):
    """
    Преобразует путь в список компонентов относительно state.dir_stack
    """
    if not state.vfs:
        return []
    if not path:
        return list(state.dir_stack)

    p = path.strip()
    if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
        p = p[1:-1]

    if p.startswith('/'):
        comp = split_path(p)
        base = []
    else:
        base = list(state.dir_stack)
        comp = split_path(p)

    for part in comp:
        if part == "." or part == "":
            continue
        if part == "..":
            if base:
                base.pop()
        else:
            base.append(part)
    return base


def resolve_node_by_path(path):
    """
    Возвращает VFSNode по заданному пути
    """
    if not state.vfs:
        return None
    parts = normalize_path(path)
    node = state.vfs.get_node(parts)
    return node


def read_text_from_node(node):
    """
    Читает текст из файла-узла
    """
    if node is None:
        return None, "No such file or directory"
    if node.is_dir:
        return None, "Is a directory"
    content = node.content or ""
    return content, None


def ls_command(arg=None):
    """
    ls [path] — перечисляет имена в директории или выводит имя файла
    """
    node = resolve_node_by_path(arg)
    if node is None:
        print_output(
            f"ls: cannot access '{arg or ''}': No such file or directory")
        return

    if node.is_dir:
        if not node.children:
            return
        for name, child in node.children.items():
            if child.is_dir:
                print_output(name + "/")
            else:
                print_output(name)
    else:
        print_output(node.name)


def cd_command(arg=None):
    """
    cd [path] — изменяет state.dir_stack
    """
    if not state.vfs:
        print_output("cd: no VFS loaded")
        return

    if not arg or arg.strip() == "":
        state.dir_stack = []
        return

    path = arg.strip()
    parts = normalize_path(path)
    node = state.vfs.get_node(parts)
    if node is None:
        print_output(f"cd: {arg}: No such file or directory")
        return
    if not node.is_dir:
        print_output(f"cd: {arg}: Not a directory")
        return

    state.dir_stack = parts


def rev_command(arg=None):
    """
    rev <file> — переворачивает символы в каждой строке и выводит их
    """
    if not arg:
        print_output("rev: missing operand")
        return
    node = resolve_node_by_path(arg)
    if node is None:
        print_output(f"rev: {arg}: No such file or directory")
        return
    if node.is_dir:
        print_output(f"rev: {arg}: Is a directory")
        return

    content, err = read_text_from_node(node)
    if err:
        print_output(f"rev: {arg}: {err}")
        return

    lines = content.splitlines()
    for line in lines:
        rev_line = line[::-1]
        print_output(rev_line.strip())


def uniq_command(arg=None):
    """
    uniq <file> — удаляет подряд идущие одинаковые строки и выводит результат
    """
    if not arg:
        print_output("uniq: missing operand")
        return
    node = resolve_node_by_path(arg)
    if node is None:
        print_output(f"uniq: {arg}: No such file or directory")
        return
    if node.is_dir:
        print_output(f"uniq: {arg}: Is a directory")
        return

    content, err = read_text_from_node(node)
    if err:
        print_output(f"uniq: {arg}: {err}")
        return

    lines = content.splitlines()
    prev = None
    for line in lines:
        if line != prev:
            print_output(line.strip())
        prev = line


def wc_command(arg=None):
    """
    wc <file> — печатает: lines words bytes
    """
    if not arg:
        print_output("0 0 0")
        return
    node = resolve_node_by_path(arg)
    if node is None:
        print_output(f"wc: {arg}: No such file or directory")
        return
    if node.is_dir:
        print_output(f"wc: {arg}: Is a directory")
        return

    content, err = read_text_from_node(node)
    if err:
        print_output(f"wc: {arg}: {err}")
        return

    lines_list = content.splitlines()
    lines_count = len(lines_list)

    words_count = 0
    for ln in lines_list:
        words_count += len(ln.split())

    bytes_count = len(content.encode('utf-8'))

    print_output(f"{lines_count} {words_count} {bytes_count}")


def exit_command():
    try:
        root.destroy()
    except Exception:
        pass
    return
