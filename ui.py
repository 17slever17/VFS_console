import tkinter as tk
from state import state

APP_TITLE = "VFS Emulator"

BG_COLOR = "#1e1e1e"
FG_COLOR = "#cfcfcf"
ENTRY_BG = "#2d2d2d"
ENTRY_FG = "#ffffff"

root = tk.Tk()
root.title(APP_TITLE)

output = tk.Text(root, height=20, state=tk.DISABLED,
                 bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
output.pack(fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Consolas", 12),
                 bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG)
entry.pack(fill=tk.X)
entry.focus_set()

def print_output(text, end="\n"):
    try:
        output.config(state=tk.NORMAL)
        output.insert(tk.END, text + end)
        output.see(tk.END)
        output.config(state=tk.DISABLED)
    except tk.TclError:
        # окно уже уничтожено
        pass

def prompt():
    path = "/" + "/".join(state.dir_stack) if state.dir_stack else "/"
    print_output(f"user@vfs:{path}$ ", end="")
