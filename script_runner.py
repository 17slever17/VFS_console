import os
from ui import print_output
from commands import run_command_line

def execute_start_script(path):
    if not path:
        return
    print_output(f"[start-script] Executing: {path}")
    if not os.path.exists(path):
        print_output(f"[start-script] ERROR: start script not found: {path}")
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print_output(f"[start-script] ERROR reading script: {e}")
        return

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped:
            print_output("")
            continue
        if stripped.startswith("#"):
            print_output(stripped)
            continue
        try:
            run_command_line(line)
        except Exception as e:
            print_output(f"[start-script] ERROR at line {idx}: {e}")
            print_output("[start-script] Execution stopped due to error.")
            return
    print_output("[start-script] Finished.")
