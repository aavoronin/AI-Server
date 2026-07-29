from project_to_file.project_to_file import project_to_file_main
from setup.copy_server_files import copy_server_files
from setup.start_server import start_wsl_server

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    project_to_file_main()
    copy_server_files()
    start_wsl_server()

