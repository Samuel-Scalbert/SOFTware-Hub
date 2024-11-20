import os
import time
from rich import print
import subprocess

def create_virtualenv(repo_path):
    """
    Create a virtual environment in the specified repository path.
    Args:
        repo_path (str): Path to the application's repository.
    """
    venv_path = os.path.join(repo_path, "venv")
    print(f"  [yellow]Creating virtual environment at: {venv_path}[/yellow]")
    try:
        subprocess.run(['python3', '-m', 'venv', venv_path], check=True)
        print(f"    [green].venv created successfully[/green]")
        return True
    except subprocess.CalledProcessError as e:
        print(f"    [red]Failed to create virtual environment: {e}[/red]")
        return False

def install_requirements(repo_path, venv_path):
    """
    Install dependencies from requirements.txt in the virtual environment.
    Args:
        repo_path (str): Path to the application's repository.
        venv_path (str): Path to the virtual environment.
    """
    requirements_file = os.path.join(repo_path, "requirements.txt")
    if not os.path.exists(requirements_file):
        print(f"    [yellow]No requirements.txt found. Skipping dependency installation.[/yellow]")
        return

    print(f"    [yellow]Installing dependencies from: {requirements_file}[/yellow]")
    pip_path = os.path.join(venv_path, "bin", "pip")
    try:
        subprocess.run([pip_path, "install", "-r", requirements_file], check=True)
        print(f"    [green]Dependencies installed successfully[/green]")
    except subprocess.CalledProcessError as e:
        print(f"    [red]Failed to install dependencies: {e}[/red]")

def client_checker(config):
    """
    Check if the applications are in the correct repositories and have a .venv folder.
    Args:
        config (dict): Configuration containing the application repository paths.
    """
    # Retrieve application details from the config

    for app_name, app_info in config.items():
        print(f"[bold][blue]---------------------------------------------[/blue][/bold]")
        print(f"[bold]Checking application: [blue]{app_name}[/blue][/bold]")

        # Check if the repository path exists
        repo_path = app_info.get('repository')
        if not repo_path:
            print(f"[red]  Repository path missing in config for {app_name}[/red]")
            continue

        print(f"  Verifying repository path: [yellow]{repo_path}[/yellow]")
        time.sleep(0.2)
        if os.path.exists(repo_path):
            print(f"    [green]Repository path exists[/green]")
        else:
            print(f"    [red]Repository path not found[/red]")
            continue

        # Check for .venv folder
        venv_path = os.path.join(repo_path, "venv")
        if venv_path != "../grobid_client_python/venv":
            print(f"  Checking for virtual environment: [yellow]{venv_path}[/yellow]")
            time.sleep(0.2)
            if os.path.exists(venv_path) and os.path.isdir(venv_path):
                print(f"    [green]venv folder found[/green]")
            else:
                print(f"    [yellow].venv not found. Creating it now...[/yellow]")
                if create_virtualenv(repo_path):
                    install_requirements(repo_path, venv_path)
                else:
                    print(f"    [red]Skipping dependency installation due to virtual environment creation failure.[/red]")

    #-----------------------------------------------test----------------------------------------------------------------
    def delete_virtualenvs(config):
        """
        Delete all virtual environments for testing purposes.
        Args:
            config (dict): Configuration containing the application repository paths.
        """
        print(f"[bold][red]Deleting all virtual environments for testing...[/red][/bold]")
        for app_name, app_info in config.items():
            repo_path = app_info.get('repository')
            venv_path = os.path.join(repo_path, "venv")
            if os.path.exists(venv_path):
                print(f"  [yellow]Deleting venv at: {venv_path}[/yellow]")
                subprocess.run(['rm', '-rf', venv_path], check=True)
                print(f"    [green]Deleted: {venv_path}[/green]")
            else:
                print(f"  [cyan]No venv found for {app_name}. Skipping.[/cyan]")

    #delete_virtualenvs(config)
print("[bold green]Application check completed.[/bold green]")
