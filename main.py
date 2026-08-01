import sys
from pathlib import Path

# Add ai-server to path to import test_server
sys.path.insert(0, str(Path(__file__).parent / "ai-server"))

from project_to_file.project_to_file import project_to_file_main
from setup.copy_server_files import copy_server_files
from setup.start_server import start_wsl_server, stop_wsl_server
from test_server import ServerTester
from ai_clients.model_client_base import ModelClientBase

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    project_to_file_main()
    copy_server_files()
    start_wsl_server()

    tester = ServerTester()
    tester.run_all()

    client = ModelClientBase()
    test_model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    print(f"\nTesting cache for {test_model_id}...")
    try:
        cache_result = client.cache_model(test_model_id)
        print("Cache result:", cache_result)

        print(f"\nTesting uncache for {test_model_id}...")
        uncache_result = client.uncache_model(test_model_id)
        print("Uncache result:", uncache_result)
    except Exception as e:
        print(f"Cache/Uncache test failed: {e}")

    stop_wsl_server()