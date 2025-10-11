class VFSNode:
    def __init__(self, name, is_dir=True, content=None):
        self.name = name
        self.is_dir = is_dir
        self.children = {} if is_dir else None
        self.content = content


class VFS:
    def __init__(self):
        self.root = VFSNode("/")

    def get_node(self, path_list):
        node = self.root
        for part in path_list:
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node


class VFSState:
    def __init__(self):
        self.dir_stack = []
        self.vfs = None
        self.start_script = None


state = VFSState()
