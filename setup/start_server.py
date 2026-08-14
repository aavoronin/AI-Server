import subprocess
import sys
import time
from pathlib import Path


def print_model_debug_info(model_id: str):
    """Print README and JSON files from the Windows cache folder when an error occurs."""
    windows_cache_dir = Path(r"D:\AIs\Cache")
    model_folder_name = model_id.replace("/", "_")
    model_dir = windows_cache_dir / model_folder_name

    print(f"- DEBUG INFO FOR {model_id} (Client Side) -")

    readme_path = model_dir / "README.md"
    if readme_path.exists():
        print("[README.md]")
        try:
            content = readme_path.read_text(encoding='utf-8')
            print(content[:4000])
        except Exception as e:
            print(f"Error reading README.md: {e}")

    for json_file in model_dir.glob("*.json"):
        if json_file.name == "model_usage.json":
            continue
        try:
            if json_file.stat().st_size <= 5120:
                print(f"[{json_file.name}]")
                print(json_file.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"Error reading {json_file.name}: {e}")

    print("- END DEBUG INFO -")


def start_wsl_server():
    """Start the AI server inside WSL from Windows."""
    wsl_distro = "Ubuntu"
    wsl_user = "av"
    wsl_workdir = "/home/av/ai-server"
    conda_env = "AI-Server"
    conda_prefix = f"/home/{wsl_user}/miniconda3/envs/{conda_env}"

    # Kill any existing process on port 8000 to prevent "address already in use"
    kill_cmd = "fuser -k 8000/tcp 2>/dev/null || true"

    # Force LD_LIBRARY_PATH to prioritize Conda and PyTorch's bundled CUDA 12.8 libraries.
    # This prevents the system from loading an older libcudart.so.12 from /usr/lib which causes
    # the "undefined symbol: cudaGetDriverEntryPointByVersion" error.
    env_setup = (
        f"export LD_LIBRARY_PATH={conda_prefix}/lib:"
        f"{conda_prefix}/lib/python3.10/site-packages/nvidia/cuda_runtime/lib:"
        f"$LD_LIBRARY_PATH"
    )

    start_cmd = f"{env_setup} && conda activate {conda_env} && cd {wsl_workdir} && python main.py"

    command = [
        "wsl",
        "-d", wsl_distro,
        "-u", wsl_user,
        "--",
        "bash", "-ic", f"{kill_cmd} && {start_cmd}"
    ]

    print("Starting AI server in WSL (Ubuntu)...")
    print(f"Working directory: {wsl_workdir}")
    print(f"Conda environment: {conda_env}")
    print("Access the server in your browser at: http://localhost:8000 or http://127.0.0.1:8000")

    try:
        subprocess.Popen(command)
        print("Server started in background. Control released.")
        time.sleep(3)
    except Exception as e:
        print(f"Failed to start server: {e}")


def stop_wsl_server():
    """Stop the AI server inside WSL."""
    wsl_distro = "Ubuntu"
    wsl_user = "av"

    command = [
        "wsl",
        "-d", wsl_distro,
        "-u", wsl_user,
        "--",
        "bash", "-c", "fuser -k 8000/tcp 2>/dev/null || true"
    ]

    print("Stopping AI server in WSL (Ubuntu)...")
    try:
        subprocess.run(command, check=True)
        print("Server stopped successfully.")
    except Exception as e:
        print(f"Failed to stop server: {e}")