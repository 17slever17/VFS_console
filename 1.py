import tkinter as tk

APP_TITLE = "VFS Emulator"

dir = []

BG_COLOR = "#1e1e1e"
FG_COLOR = "#cfcfcf"
ENTRY_BG = "#2d2d2d"
ENTRY_FG = "#ffffff"

def print_output(text, end="\n"):
    output.config(state=tk.NORMAL)
    output.insert(tk.END, text + end)
    output.see(tk.END)
    output.config(state=tk.DISABLED)

def prompt():
    print_output(f"user@vfs:{'/' + '/'.join(dir)}$ ", end="")

def run_command(event=None):
    global dir
    cmd_line = entry.get()
    entry.delete(0, tk.END)
    print_output(cmd_line)

    if not cmd_line.strip():
        prompt()
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
            pass
        elif " " in args and args[0] != '"' and args[-1] != '"':
            print_output("cd: too many arguments")
        else:
            if args[0] == '"' and args[-1] == '"':
                args = args[1:-1].split('/')
            else:
                args = args.split('/')
            
            new_dir = dir
            for arg in args:
                if arg == "":
                    new_dir = []
                elif arg == "..":
                    if new_dir:
                        new_dir.pop()
                    if args[1] == "":
                        break
                elif arg == ".":
                    new_dir = dir
                else:
                    new_dir.append(arg)
            dir = new_dir
    elif cmd == "exit":
        root.destroy()
        return
    else:
        print_output(f"Unknown command: {cmd}")

    prompt()

root = tk.Tk()
root.title(APP_TITLE)

output = tk.Text(root, height=20, state=tk.DISABLED, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)

output.pack(fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Consolas", 12), bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG)
entry.pack(fill=tk.X)
entry.bind("<Return>", run_command)
entry.focus_set()

print_output("VFS Emulator (prototype)\nCommands: ls, cd, exit\n")
prompt()

root.mainloop()
