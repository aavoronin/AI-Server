import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from setup.copy_server_files import copy_server_files
from project_to_file.project_to_file import project_to_file_main
from setup.start_server import start_wsl_server, stop_wsl_server
from setup.run_model_benchmark import run_model_benchmark, run_model_benchmark_json
from setup.run_models_on_vacancies import run_models_on_vacancies
from setup.test_server import ServerTester

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    project_to_file_main()
    copy_server_files()
    start_wsl_server()

    tester = ServerTester()
    tester.run_all()

    if True:
        run_models_on_vacancies(3, r"C:\Py\AI-Server\test_cases\test_vacancies\02")
        #run_models_on_vacancies(1, r"C:\Py\AI-Server\test_cases\test_vacancies\01")
        #run_models_on_vacancies(2, r"C:\Py\AI-Server\test_cases\test_vacancies\01")
    stop_wsl_server()

    start_wsl_server()

    #run_model_benchmark()
    #run_model_benchmark_json()

    stop_wsl_server()