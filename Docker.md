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

[For More Info, Check Docker Guide.](https://docs.docker.com/engine/reference/commandline/images/)


Using Dockerfiles
-----------------

Also we can use a Dockerfile to build a new image:

```bash
# Create App Folder
$ mkdir app
```

Then Create Dockerfile to Install PHP stuff `app/Dockerfile`.

```bash
FROM ubuntu:18.04

LABEL maintainer="Clivern"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y gnupg tzdata \
    && echo "UTC" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update \
    && apt-get install -y curl zip unzip git supervisor sqlite3 \
       nginx php7.2-fpm php7.2-cli \
       php7.2-pgsql php7.2-sqlite3 php7.2-gd \
       php7.2-curl php7.2-memcached \
       php7.2-imap php7.2-mysql php7.2-mbstring \
       php7.2-xml php7.2-zip php7.2-bcmath php7.2-soap \
       php7.2-intl php7.2-readline php7.2-xdebug \
       php-msgpack php-igbinary \
    && php -r "readfile('http://getcomposer.org/installer');" | php -- --install-dir=/usr/bin/ --filename=composer \
    && mkdir /run/php \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
```

Then let's build our image

```bash
$ docker build -t clivern/app:latest -f app/Dockerfile app/
```

Now we can build container from that image `clivern/app:latest`

```bash
$ docker run -it clivern/app bash
```

If we want to add some files to nginx after installation

```bash
FROM ubuntu:18.04

LABEL maintainer="Clivern"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y gnupg tzdata \
    && echo "UTC" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update \
    && apt-get install -y curl zip unzip git supervisor sqlite3 \
       nginx php7.2-fpm php7.2-cli \
       php7.2-pgsql php7.2-sqlite3 php7.2-gd \
       php7.2-curl php7.2-memcached \
       php7.2-imap php7.2-mysql php7.2-mbstring \
       php7.2-xml php7.2-zip php7.2-bcmath php7.2-soap \
       php7.2-intl php7.2-readline php7.2-xdebug \
       php-msgpack php-igbinary \
    && php -r "readfile('http://getcomposer.org/installer');" | php -- --install-dir=/usr/bin/ --filename=composer \
    && mkdir /run/php \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && echo "daemon off;" >> /etc/nginx/nginx.conf

ADD default /etc/nginx/sites-available/default
```

Then create the default virualhost file inside app to be `app/default`:

```bash
server {
    listen 80 default_server;

    root /var/www/html/public;

    index index.html index.htm index.php;

    server_name _;

    charset utf-8;

    location = /favicon.ico { log_not_found off; access_log off; }
    location = /robots.txt  { log_not_found off; access_log off; }

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php7.2-fpm.sock;
    }

    error_page 404 /index.php;
}
```

ENTRYPOINT or CMD
-----------------

Basically both `ENTRYPOINT` and `CMD` give you a way to identify which executable should be run when a container is started from your image

For example, let's say that we have the following Dockerfile

```bash
FROM ubuntu:trusty
CMD ["/bin/ping","localhost"]

# Then Build The Image
docker build -t app .
```

We can create a container that run this command `/bin/ping localhost` or override it.

```bash
$ docker run -it app
PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.043 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.097 ms

# Override it with bash
$ docker run -it app bash
```

Also the same could happen to `ENTRYPOINT`.

```bash
FROM ubuntu:trusty
ENTRYPOINT ["/bin/ping","localhost"]

# Then Build The Image
docker build -t app .
```

Then you can run a container as interactive or daemon.
```bash
# interactive
$ docker run -it app

# daemon
$ docker run -d app
```

the recommendation is use `CMD` in your Dockerfile when you want the user of your image to have the flexibility to run whichever executable they choose when starting the container. 
In contrast, `ENTRYPOINT` should be used in scenarios where you want the container to behave exclusively as if it were the executable it's wrapping. That is, when you don't want or expect the user to override the executable you've specified.

For More Info, [Please read this guide.](https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/)


Networks
--------

We can create a network for containers to be added to:

```bash
# List networks
$ docker network ls

# Create a network
$ docker network create appnet
```

Then Create a MySQL Container

```bash
$ docker run -d \
    --name=mysql \
    --network=appnet \
    -e MYSQL_ROOT_PASSWORD=root \
    -e MYSQL_DATABASE=homestead \
    -e MYSQL_USER=homestead \
    -e MYSQL_USER_PASSWORD=secret \
    mysql:5.7
```

Then Create App Container and Connected to the same network `appnet`.

```bash
# Create a Docker File
FROM ubuntu:trusty
ENTRYPOINT ["/bin/ping","mysql"]

# Then Build The Image
docker build -t app .

# Then Create Container of That Image
$ docker run -d \
    --name=app \
    --network=appnet \
     app
```

You can access the app container with the following command

```bash
$ docker exec -it app bash

$ ping mysql
PING mysql (172.18.0.2) 56(84) bytes of data.
64 bytes from mysql.appnet (172.18.0.2): icmp_seq=1 ttl=64 time=0.173 ms
64 bytes from mysql.appnet (172.18.0.2): icmp_seq=2 ttl=64 time=0.130 ms

$ getent hosts mysql
172.18.0.2      mysql

$ apt-get install mysql-client

$ mysql -h 172.18.0.2 -u root -p
Enter password: root
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.22 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| homestead          |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

Add another container which is published on port `8080`

```bash
$ docker create --name my-nginx \
    --network appnet \
    --publish 8080:80 \
    nginx:latest

# You should be able to see nginx on host machine on port 8080
$ docker start my-nginx
```

You can connect and disconnect containers from network like this:

```bash
$ docker network disconnect appnet app
$ docker network connect appnet app
```

You can also inspect the container or the network to get some info about container network or containers connected to same network or even ip of container to access from another.

```bash
$ docker inspect app
$ docker network inspect appnet
```

Replace and Connect containers to a new network.

```bash
$ docker network disconnect appnet app
$ docker network disconnect appnet mysql

# Create a network
$ docker network create appnet2

# Connect to a new network
$ docker network connect appnet2 app
$ docker network connect appnet2 mysql

# Restart Container
$ docker restart app mysql

# This shall show connected containers
$ docker network inspect appnet2
```

[For More Info, Check Networks Guide.](https://docs.docker.com/network/)


Docker Storage
--------------

### Volumes

```bash
# Create a Volume
$ docker volume create my-vol

# List Volumes
$ docker volume ls

# Inspect Volume
$ docker volume inspect my-vol

# Remove a Volume
$ docker volume rm my-vol

# To remove all unused volumes and free up space
$ docker volume prune

# Start a container with a volume (Host machine path will be /var/lib/docker/volumes/nginx-vol-1/_data)
$ docker run -d \
    --name=nginx1 \
    --mount source=nginx-vol-1,destination=/usr/share/nginx/html \
    --publish 8000:80 \
    nginx:latest

# Inspect Docker Container
$ docker container inspect nginx1

# Stop the container and remove the volume. Note volume removal is a separate step.
$ docker container stop nginx1
$ docker container rm nginx1
$ docker volume rm nginx-vol-1

# Use a read-only volume
$ docker run -d \
    --name=nginx2 \
    --mount source=nginx-vol-2,destination=/usr/share/nginx/html,readonly \
    --publish 8000:80 \
    nginx:latest

# Backup a container volume as tar
$ docker run --rm --volumes-from nginx1 -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /usr/share/nginx/html
```

### Bind mounts

```bash
$ mkdir app
$ echo "Hello World" > app/README.md

# Bind mount to container
$ docker run -d \
    --name=nginx1 \
    --mount type=bind,source="$(pwd)"/app,target=/app \
    --publish 8000:80 \
    nginx:latest

# Use a read-only bind mount
$ docker run -d \
    --name=nginx1 \
    --mount type=bind,source="$(pwd)"/app,target=/app,readonly \
    --publish 8000:80 \
    nginx:latest

$ docker exec -it nginx1 bash
$ ls ./app
```

### `tmpfs` mounts

As opposed to volumes and bind mounts, a `tmpfs` mount is temporary, and only persisted in the host memory. When the container stops, the `tmpfs` mount is removed, and files written there won’t be persisted.

```bash
$ docker run -d \
    --name=nginx1 \
    --mount type=tmpfs,destination=/app \
    --publish 8000:80 \
    nginx:latest

# Inspect Docker Container
$ docker container inspect nginx1

$ docker exec -it nginx1 bash
$ ls ./app
$ echo "Hello World" > app/README.md
$ exit
$ docker restart nginx1 # This should clear the README.md file
```


Limiting Container's Resources
------------------------------

* [Resource Constraints.](https://docs.docker.com/v17.09/engine/admin/resource_constraints/)
* [Kernel doesn't Support cgroup Swap Limit Capabilities.](https://docs.docker.com/install/linux/linux-postinstall/#your-kernel-does-not-support-cgroup-swap-limit-capabilities)


Recap and Cheat Sheet
---------------------
```bash
## List Docker CLI commands
$ docker
$ docker container --help

## Display Docker version and info
$ docker --version
$ docker version
$ docker info

## Execute Docker image
$ docker run hello-world

## List Docker images
$ docker image ls

## List Docker containers (running, all, all in quiet mode)
$ docker container ls
$ docker container ls --all
$ docker container ls -aq

$ docker build -t friendlyhello .  # Create image using this directory's Dockerfile
$ docker run -p 4000:80 friendlyhello  # Run "friendlyname" mapping port 4000 to 80
$ docker run -d -p 4000:80 friendlyhello         # Same thing, but in detached mode
$ docker container ls                                # List all running containers
$ docker container ls -a             # List all containers, even those not running
$ docker container stop <hash>           # Gracefully stop the specified container
$ docker container kill <hash>         # Force shutdown of the specified container
$ docker container rm <hash>        # Remove specified container from this machine
$ docker container rm $(docker container ls -a -q)         # Remove all containers
$ docker image ls -a                             # List all images on this machine
$ docker image rm <image id>            # Remove specified image from this machine
$ docker image rm $(docker image ls -a -q)   # Remove all images from this machine
$ docker login             # Log in this CLI session using your Docker credentials
$ docker tag <image> username/repository:tag  # Tag <image> for upload to registry
$ docker push username/repository:tag            # Upload tagged image to registry
$ docker run username/repository:tag                   # Run image from a registry

# Get Logs with Stream
$ docker logs --follow <container-name>

# Get a live data stream for running containers
$ docker stats

# Get a live data stream for one or two containers
$ docker stats <container_name> <?container_name>

# Get a live CPU & Memory Stats for one or more containers
$ docker stats --all --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" <container_name> <?container_name>

# Get a live CPU & Memory Stats ... etc for one or more containers
$ docker stats --all --format "table {{.Container}}\t{{.Name}}\t{{.ID}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.MemPerc}}\t{{.PIDs}}" <container_name> <?container_name>

# Inspect the changes to container
$ docker diff <container_name>

# Get Docker Events
$ docker events --format '{{json .}}'

# Get Docker Events With Filter
$ docker events --filter 'type=container' --format 'Type={{.Type}}  Status={{.Status}}  ID={{.ID}}'
$ docker events --since '2017-01-05'
$ docker events --filter 'event=stop'
$ docker events --filter 'image=alpine'
$ docker events --filter 'container=test'
$ docker events --filter 'container=test' --filter 'container=container_id'
$ docker events --filter 'container=test' --filter 'event=stop'
$ docker events --filter 'type=volume'
$ docker events --filter 'type=network'
$ docker events --filter 'container=container_1' --filter 'container=container_2'
$ docker events --filter 'type=volume'
$ docker events --filter 'type=network'
$ docker events --filter 'type=plugin'
$ docker events -f type=service
$ docker events -f type=node
$ docker events -f type=secret
$ docker events -f type=config
$ docker events --filter 'scope=swarm'
```
