import argparse
import tkinter as tk
from ui import root, entry, print_output, prompt
from commands import run_command_line, load_vfs_from_xml
from script_runner import execute_start_script
from vfs import state


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

    print_output("VFS Emulator (prototype)\nCommands: ls, cd, exit, vfs-save\n")
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


if __name__ == "__main__":
    entry.bind("<Return>", run_command)
    parse_and_start()
    root.mainloop()
