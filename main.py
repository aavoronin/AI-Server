import sys
from pathlib import Path

# Add ai-server to path to import test_server
sys.path.insert(0, str(Path(__file__).parent / "ai-server"))

from project_to_file.project_to_file import project_to_file_main
from setup.copy_server_files import copy_server_files
from setup.start_server import start_wsl_server, stop_wsl_server
from setup.run_model_benchmark import run_model_benchmark, run_model_benchmark_json, run_models_on_vacancies
from test_server import ServerTester


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    project_to_file_main()
    copy_server_files()
    start_wsl_server()

    tester = ServerTester()
    tester.run_all()

    run_models_on_vacancies(r"C:\Py\AI-Server\test_cases\test_vacancies\01")
    #run_model_benchmark_json()
    #run_model_benchmark()

    stop_wsl_server()