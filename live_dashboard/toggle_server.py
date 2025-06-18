import subprocess
import os
import signal
import sys
import time
import webbrowser

# Files used for tracking server state
PID_FILE = 'server.pid'
LOG_FILE = 'server.log'

# URL to open when server starts
LOCAL_URL = 'http://127.0.0.1:8000/'

def get_pid():
    """Read the server PID from file."""
    if not os.path.exists(PID_FILE):
        return None
    with open(PID_FILE, 'r') as f:
        try:
            return int(f.read().strip())
        except ValueError:
            return None

def is_running(pid):
    """Check if a process with given PID is running."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def start():
    """Start the Django server in the background."""
    pid = get_pid()
    if pid and is_running(pid):
        print(f"Server is already running with PID {pid}.")
        return

    print("Starting server...")
    with open(LOG_FILE, 'a') as log_file:
        process = subprocess.Popen(
            [sys.executable, 'manage.py', 'runserver'], # sys.exe returns full path to the python interpreter that is currently running your script
            stdout=log_file,
            stderr=log_file,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # Windows only
        )
        with open(PID_FILE, 'w') as f:
            f.write(str(process.pid))

        print(f"Server started with PID {process.pid}.")
        time.sleep(2)
        webbrowser.open(LOCAL_URL)

def stop():
    """Stop the Django server using the stored PID."""
    pid = get_pid()
    if not pid:
        print("No PID file found. Server may not be running.")
        return

    if not is_running(pid):
        print(f"No process found with PID {pid}. Removing stale PID file.")
        os.remove(PID_FILE)
        return

    try:
        os.kill(pid, signal.CTRL_BREAK_EVENT)
        time.sleep(1)
        os.remove(PID_FILE)
        print(f"Server with PID {pid} stopped.")
    except Exception as e:
        print(f"Error stopping server: {e}")

def restart():
    """Restart the server."""
    print("Restarting server...")
    stop()
    time.sleep(1)
    start()

def status():
    """Check server running status."""
    pid = get_pid()
    if pid and is_running(pid):
        print(f"✅ Server is running with PID {pid}.")
    else:
        print("❌ Server is not running.")

def main():
    """Handle command-line arguments."""
    if len(sys.argv) != 2 or sys.argv[1] not in ['start', 'stop', 'restart', 'status']:
        print("Usage: python toggle_server.py [start|stop|restart|status]")
        return

    command = sys.argv[1]
    if command == 'start':
        start()
    elif command == 'stop':
        stop()
    elif command == 'restart':
        restart()
    elif command == 'status':
        status()

if __name__ == '__main__':
    main()
