import os
import signal
import subprocess
import sys
import time
from shutil import which

SERVER_CMD = ["briefcase", "run", "web", "--no-browser"]
# TEST_CMD = ["pytest", "tests"]

# Quieter output ('-rN' to remove 'short test summary info')
TEST_CMD = ["pytest", "--tb=no", "--disable-warnings", "-rN", "tests"]
STARTUP_WAIT_SECS = float(os.getenv("SERVER_STARTUP_SECS", "5.0"))

IS_WINDOWS = os.name == "nt"
CREATE_NEW_PROCESS_GROUP = 0x00000200 if IS_WINDOWS else 0


def start_server():
    if which(SERVER_CMD[0]) is None:
        print(f"Error: '{SERVER_CMD[0]}' not found on PATH.", file=sys.stderr)
        sys.exit(127)
    kwargs = {}
    if IS_WINDOWS:
        kwargs["creationflags"] = CREATE_NEW_PROCESS_GROUP
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.STDOUT
    return subprocess.Popen(SERVER_CMD, **kwargs)


def stop_server(proc, timeout=10):
    if proc.poll() is not None:
        return
    try:
        if IS_WINDOWS:
            # Try to be gentle first
            try:
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            except Exception:
                proc.terminate()
        else:
            proc.send_signal(signal.SIGINT)
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            proc.kill()


def main():
    print("> Starting web server:", " ".join(SERVER_CMD))
    server = start_server()

    try:
        time.sleep(STARTUP_WAIT_SECS)
        print("> Running tests:", " ".join(TEST_CMD))
        result = subprocess.run(TEST_CMD)
        exit_code = result.returncode
    except KeyboardInterrupt:
        print("\n> Interrupted by user.", file=sys.stderr)
        exit_code = 130
    finally:
        print("> Shutting down web server…")
        stop_server(server)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
