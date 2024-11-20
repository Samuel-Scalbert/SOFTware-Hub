import time
from rich import print
import subprocess
import docker

def docker_image(docker_config, client):

    # Retrieve the list of needed tags from the config
    list_needed_tags = [container_tag['tag'] for container_tag in docker_config.values()]

    # Retrieve the list of images available on the VM
    available_imgs = [tag for img in client.images.list() for tag in img.tags]

    # Check if the VM has the correct images
    for needed_tag in list_needed_tags:
        print(f"[bold]Checking (image): [blue]{needed_tag.replace(':', ':')}[/bold]")
        time.sleep(.2)
        if needed_tag not in available_imgs:
            points = " " * (50 - len("Downloading the image "))
            print(f"    Downloading the image {points}", end="\r")
            points = " " * (50 - len(needed_tag))
            client.images.pull(needed_tag)
            print(f"    [white]{needed_tag}[/white]{points}", end="")
            print("     [bold green]available[/bold green]")
        else:
            points = " " * (50 - len(needed_tag))
            print(f"    [white]{needed_tag}[/white]{points} [green]available[/green]")

def manage_containers(image_name):
    client = docker.from_env()

    # List all containers using the specified image
    containers = [container for container in client.containers.list(all=True) if image_name in container.image.tags]
    if not containers:
        print(f"No containers found for image: {image_name}", end="\r")
        return image_name

    # Sort containers by creation time (oldest first)
    containers.sort(key=lambda c: c.attrs['Created'])

    # Identify the oldest container
    oldest_container = containers[0]

    # Remove all other containers that use the same image
    for container in containers[1:]:
        container.stop()
        container.remove()

    if len(oldest_container.attrs['NetworkSettings']['Ports']) <= 0:
        oldest_container.stop()
        oldest_container.remove()
        print(f"No containers found for image: {image_name}", end="\r")
        return image_name

    print(f"Kept container: '{oldest_container.name}' running with image [bold green]{image_name}[/bold green] on port :{oldest_container.attrs['NetworkSettings']['Ports']}")


def gpu_checker():
    try:
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'])
        gpus = output.decode().strip().split('\n')
        if gpus:
            print(f"GPUs found: {gpus}")
            return True
        else:
            print("[red]No GPUs found.[/red]")
            return False
    except FileNotFoundError:
        print("[red]nvidia-smi not found. No NVIDIA GPU is available or the NVIDIA drivers are not installed.[/red]")
        return False

def docker_container_launcher(image, port, client, gpu):
    if gpu == True:
        container = client.containers.run(
            image,  # Replace with your Docker image name
            detach=True,  # Equivalent to -d
            remove=True,  # Equivalent to --rm
            init=True,  # Equivalent to --init
            ulimits=[docker.types.Ulimit(name='core', soft=0, hard=0)],  # Equivalent to --ulimit core=0
            ports=port,
            device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])],
        )

        print(f"Container '{container.name}' started with image [bold green]{image}[/bold green], on the port : {port}.")
    else:
        container = client.containers.run(
            image,  # Replace with your Docker image name
            detach=True,  # Equivalent to -d
            remove=True,  # Equivalent to --rm
            init=True,  # Equivalent to --init
            ulimits=[docker.types.Ulimit(name='core', soft=0, hard=0)],  # Equivalent to --ulimit core=0
            ports=port,
        )

        print(f"Container '{container.name}' started with image [bold green]{image}[/bold green], on the port : {port}.")


def docker_container(docker_config, client):
    gpu = gpu_checker()

    image_needed = manage_containers("grobid/grobid:0.8.0")
    if image_needed :
        docker_container_launcher(image_needed, {'8070/tcp': 8070}, client, gpu)

    image_needed = manage_containers("grobid/software-mentions:0.8.0")
    if image_needed :
        docker_container_launcher(image_needed, {'8060/tcp': 8060}, client, gpu)

    return None