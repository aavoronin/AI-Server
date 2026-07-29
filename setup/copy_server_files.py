import shutil
from pathlib import Path


def copy_server_files():
    src_dir = Path(r"C:\Py\AI-Server\ai-server")
    dst_dir = Path(r"\\wsl.localhost\Ubuntu\home\av\ai-server")

    if not src_dir.exists():
        print(f"Source directory does not exist: {src_dir}")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0

    for src_file in src_dir.rglob("*"):
        if not src_file.is_file():
            continue

        rel_path = src_file.relative_to(src_dir)
        dst_file = dst_dir / rel_path

        dst_file.parent.mkdir(parents=True, exist_ok=True)

        if dst_file.exists():
            src_mtime = src_file.stat().st_mtime
            dst_mtime = dst_file.stat().st_mtime
            if src_mtime <= dst_mtime:
                skipped += 1
                continue

        shutil.copy2(src_file, dst_file)
        copied += 1
        print(f"Copied: {rel_path}")

    print(f"Copy complete. Copied: {copied}, Skipped: {skipped}")