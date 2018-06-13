# Docker


Install Docker
--------------

To install docker on Ubuntu.

```bash
$ apt-get update
$ sudo apt install docker.io
```

Then ensure that it is enabled to start after reboot:

```bash
$ sudo systemctl enable docker
```

Working With Images
-------------------
Docker images are essentially a snapshot of a container. we're going to explore Docker images a bit more:

```bash
# To List Images
$ docker images

# To Remove Image
$ docker rmi <image_name>

# Getting a new Image
docker pull ubuntu:18.04

# Searching Docker Images
docker search <term>

# Create a new Image
$ docker run -it ubuntu:18.04 bash
# Then Inside docker install for example nginx
$ apt-get update
$ apt-get install -y nginx
# Get Container ID
$ docker ps -a
# In another Terminal Get the Diff and Create the Image
$ docker diff <container_id> 
$ docker commit -a "Clivern" -m "Nginx installed" <container_id> clivernnginx:latest

# Then you able to see your new image
$ docker images

# Publishing an Image to Docker Hub (https://hub.docker.com)
$ docker login

# Create Image Tag
$ docker tag <image_id> <account_name>/clivernnginx:ubuntu

# Then Push the Image to Docker Hub
$ docker push <account_name>/clivernnginx
```
