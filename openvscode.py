import subprocess
import os
import time
import ctypes
import sys
import win32serviceutil

def is_admin():
    """
    Check if the script is running with administrator privileges.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def start_service(service_name):
    """
    Start a Windows service if it is not already running.
    """
    try:
        # Check the status of the service
        service_status = win32serviceutil.QueryServiceStatus(service_name)[1]

        if service_status == 4:  # 4 means running
            print(f"{service_name} service is already running.")
        else:
            print(f"Starting {service_name} service...")
            win32serviceutil.StartService(service_name)
            time.sleep(2)  # Give some time for the service to start
            print(f"{service_name} service started.")
    except Exception as e:
        print(f"Failed to start {service_name} service: {e}")

def open_vscode(folder_path):
    """
    Open Visual Studio Code with a given folder.
    """
    try:
        # Full path to VS Code executable
        vscode_path = r"C:\Users\Milind\AppData\Local\Programs\Microsoft VS Code\Code.exe"  # Adjust path if needed
        print(f"Opening Visual Studio Code with folder: {folder_path}")
        subprocess.run([vscode_path, folder_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to open Visual Studio Code: {e}")
    except FileNotFoundError as e:
        print(f"VS Code executable not found: {e}")

if __name__ == "__main__":
    # Specify the folder path to open in VS Code
    folder_path = r"C:\Users\Milind\Desktop\projects\LoginApp_py"

    # Check if the script is run as an administrator
    if is_admin():
        # Start the MySQL80 service
        start_service("MySQL80")

        # Open Visual Studio Code with the specified folder
        open_vscode(folder_path)
    else:
        print("This script needs to be run as an Administrator.")
        # Prompt to rerun the script as an administrator
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
