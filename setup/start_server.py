import subprocess
import sys


def start_wsl_server():
    """Start the AI server inside WSL from Windows."""
    wsl_distro = "Ubuntu"
    wsl_user = "av"
    wsl_workdir = "/home/av/ai-server"
    conda_env = "AI-Server"

    command = [
        "wsl",
        "-d", wsl_distro,
        "-u", wsl_user,
        "--",
        "bash", "-ic", f"conda activate {conda_env} && cd {wsl_workdir} && python main.py"
    ]

    print(f"Starting AI server in WSL ({wsl_distro})...")
    print(f"Working directory: {wsl_workdir}")
    print(f"Conda environment: {conda_env}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start server in WSL. Error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("WSL is not installed or 'wsl' command not found.")
        sys.exit(1)