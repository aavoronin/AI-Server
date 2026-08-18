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
