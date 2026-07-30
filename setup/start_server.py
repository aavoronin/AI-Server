import subprocess
import sys


def start_wsl_server():
    """Start the AI server inside WSL from Windows."""
    wsl_distro = "Ubuntu"
    wsl_user = "av"
    wsl_workdir = "/home/av/ai-server"
    conda_env = "AI-Server"

    # Kill any existing process on port 8000 to prevent "address already in use"
    kill_cmd = "fuser -k 8000/tcp 2>/dev/null || true"
    start_cmd = f"conda activate {conda_env} && cd {wsl_workdir} && python main.py"

    command = [
        "wsl",
        "-d", wsl_distro,
        "-u", wsl_user,
        "--",
        "bash", "-ic", f"{kill_cmd}; {start_cmd}"
    ]

    print(f"Starting AI server in WSL ({wsl_distro})...")
    print(f"Working directory: {wsl_workdir}")
    print(f"Conda environment: {conda_env}")
    print("Access the server in your browser at: http://localhost:8000 or http://127.0.0.1:8000")

    try:
        subprocess.Popen(command)
        print("Server started in background. Control released.")
    except FileNotFoundError:
        print("WSL is not installed or 'wsl' command not found.")
        sys.exit(1)


def stop_wsl_server():
    """Stop the AI server running inside WSL."""
    wsl_distro = "Ubuntu"
    wsl_user = "av"

    command = [
        "wsl",
        "-d", wsl_distro,
        "-u", wsl_user,
        "--",
        "bash", "-c", "fuser -k 8000/tcp 2>/dev/null || true"
    ]

    print("Stopping AI server in WSL...")
    try:
        subprocess.run(command, check=True)
        print("Server stopped successfully.")
    except Exception as e:
        print(f"Failed to stop server: {e}")