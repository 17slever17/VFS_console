class VFSState:
    def __init__(self):
        self.dir_stack = []
        self.vfs_root = None
        self.start_script = None

state = VFSState()
