import json
import docker
from rich import print
from DOCKER import docker_image, docker_container
import subprocess
from CLIENT import client_checker


def load_config(file_path):
    """Load configuration from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[bold red]Configuration file not found! Exiting.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"[bold red]Error parsing configuration file: {e}")
        exit(1)


def clean_up_containers(client):
    """Remove all containers forcefully."""
    try:
        for container in client.containers.list(all=True):
            print(f"[yellow]Removing container: {container.name}[/yellow]")
            container.remove(force=True)
        print("[green]All containers removed successfully.[/green]")
    except docker.errors.APIError as e:
        print(f"[bold red]Error during container cleanup: {e}[/bold red]")


def main():
    # Load the configuration
    config_path = 'config.json'
    config = load_config(config_path)
    docker_config = config.get('Docker', {})
    client_config = config.get('Client', {})

    # Display banner
    message = """
    ┏┓┏┓┏┓┏┳┓           ┓┏  ┓ 
    ┗┓┃┃┣  ┃ ┓┏┏┏┓┏┓┏┓━━┣┫┓┏┣┓
    ┗┛┗┛┻  ┻ ┗┻┛┗┻┛ ┗   ┛┗┗┻┗┛                      
    """
    print(message)

    # Initialize Docker client
    client = docker.from_env()

    '''# Testing Purpose
    print("[bold red]------------------------------------------")
    print("[bold red] TESTING PURPOSE:")
    try:
        for x in range(4):
            test_open_container_bad(client)
        #test_open_container_good(client)
    except Exception as e:
        print(f"[bold red]Error during testing: {e}[/bold red]")
    print("[bold red]------------------------------------------")'''

    # Uncomment the following line if you need to validate Docker images
    docker_image(docker_config, client)

    # Manage and run Docker containers
    try:
        docker_container(docker_config, client)
    except Exception as e:
        print(f"[bold red]Error managing Docker containers: {e}[/bold red]")

    # check for Grobid/Softcite Client

    try:
        client_checker(client_config)
    except Exception as e:
        print(f"[bold red]Error with the Grobid's and/or Softcite's clients: {e}[/bold red]")

    # Cleanup all containers
    # clean_up_containers(client)


if __name__ == '__main__':
    main()
