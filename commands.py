from ui import print_output, root
from state import state

def run_command_line(cmd_line):
    print_output(cmd_line)
    if not cmd_line.strip():
        return

    parts = cmd_line.strip().split(maxsplit=1)
    cmd = parts[0]
    args = parts[1].strip() if len(parts) > 1 else []

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
