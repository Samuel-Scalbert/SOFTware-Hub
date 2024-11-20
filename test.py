from rich import print

def test_open_container_bad(client):
    container = client.containers.run(
        'hello-world:latest',
        detach=True,
    )
    print(f"Container {container.name} started with image : [red] {container.image}.")

def test_open_container_good(client):
    container = client.containers.run(
        'grobid/grobid:0.8.0',
        detach=True,
    )
    print(f"Container {container.name} started with image : [red] {container.image}.")