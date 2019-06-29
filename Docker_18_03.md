<p align="center">
    <img alt="Docker Logo" src="https://cdn.worldvectorlogo.com/logos/docker-1.svg" height="80" />
</p>


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


Dockerfile
----------
Docker can build images automatically by reading the instructions from a `Dockerfile`. A `Dockerfile` is a text document that contains all the commands a user could call on the command line to assemble an image.

```bash
docker build -t clivern/app .
```

Here is the format of the Dockerfile:

```dockerfile
# Comment
INSTRUCTION arguments
```

### FROM

The `FROM` instruction initializes a new build stage and sets the Base Image for subsequent instructions.

```dockerfile
FROM <image> [AS <name>]

## Or

FROM <image>[:<tag>] [AS <name>]

## Or

FROM <image>[@<digest>] [AS <name>]

## Or

FROM nginx:latest
```

### RUN

The `RUN` instruction will execute any commands in a new layer on top of the current image and commit the results. The resulting committed image will be used for the next step in the `Dockerfile`.

`RUN` has 2 forms:

* `RUN <command>` (shell form, the command is run in a shell, which by default is `/bin/sh -c` on Linux or `cmd /S /C` on Windows)
* `RUN ["executable", "param1", "param2"]` (exec form)

```dockerfile
## One Line Command
RUN apt-get update

## Two Lines Command
RUN apt-get update \
    apt-get install git

RUN echo "Hello World"

## To use a different shell, other than /bin/sh, use the exec form passing in the desired shell.
RUN ["/bin/bash", "-c", "echo hello"]
```

### CMD

The CMD instruction has three forms:

* `CMD ["executable","param1","param2"]` (exec form, this is the preferred form)
* `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT)
* `CMD command param1 param2` (shell form)


There can only be one `CMD` instruction in a `Dockerfile`. If you list more than one `CMD` then only the last `CMD` will take effect.

The main purpose of a `CMD` is to provide defaults for an executing container. These defaults can include an executable, or they can omit the executable, in which case you must specify an `ENTRYPOINT` instruction as well.

*Note: Don’t confuse `RUN` with `CMD`. `RUN` actually runs a command and commits the result; `CMD` does not execute anything at build time, but specifies the intended command for the image.*

### LABEL

The `LABEL` instruction adds metadata to an image.

```dockerfile
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."

LABEL multi.label1="value1" multi.label2="value2" other="value3"
```

### MAINTAINER (deprecated)

Use `LABEL` Instead.

### EXPOSE

The `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime. You can specify whether the port listens on `TCP` or `UDP`, and the default is `TCP` if the protocol is not specified.

```dockerfile
EXPOSE <port> [<port>/<protocol>...]

EXPOSE 80
# OR
EXPOSE 80/tcp
# OR
EXPOSE 80/udp
```

Regardless of the `EXPOSE` settings, you can override them at runtime by using the `-p` flag.

```bash
docker run -p 80:80/tcp ...
```

### ENV

The `ENV` instruction sets the environment variable `<key>` to the value `<value>`. This value will be in the environment for all subsequent instructions in the build stage and can be replaced inline in many as well.

```dockerfile
ENV myName John Doe
ENV myDog Rex The Dog
ENV myCat fluffy
```

```bash
# Override ENV vars
docker run --env <key>=<value>
```

### ADD

The `ADD` instruction copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.

`ADD` has two forms:
* `ADD [--chown=<user>:<group>] <src>... <dest>`
* `ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]` (this form is required for paths containing whitespace)

The `--chown` feature is only supported on `Dockerfiles` used to build Linux containers.

```dockerfile
ADD test relativeDir/          # adds "test" to `WORKDIR`/relativeDir/
ADD test /absoluteDir/         # adds "test" to /absoluteDir/

ADD --chown=www-data:www-data test relativeDir/          # adds "test" to `WORKDIR`/relativeDir/
```

### COPY

The `COPY` instruction copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.

COPY has two forms:
* `COPY [--chown=<user>:<group>] <src>... <dest>`
* `COPY [--chown=<user>:<group>] ["<src>",... "<dest>"]` (this form is required for paths containing whitespace).

The `--chown` feature is only supported on `Dockerfiles` used to build Linux containers.

```dockerfile
COPY test relativeDir/   # adds "test" to `WORKDIR`/relativeDir/
COPY test /absoluteDir/  # adds "test" to /absoluteDir/

COPY --chown=www-data:www-data test relativeDir/          # adds "test" to `WORKDIR`/relativeDir/
```

### ENTRYPOINT

An `ENTRYPOINT` allows you to configure a container that will run as an executable.

`ENTRYPOINT` has two forms:
* `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, preferred)
* `ENTRYPOINT command param1 param2` (shell form)

You can override the `ENTRYPOINT` instruction using the `docker run --entrypoint` flag.

```dockerfile
# You can see that top is the only process
FROM ubuntu
ENTRYPOINT ["top", "-b"]

## OR

FROM ubuntu
ENTRYPOINT ["ping", "8.8.8.8"]
```

### VOLUME

The `VOLUME` instruction creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers.

```dockerfile
FROM ubuntu
RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol
```

### USER

The `USER` instruction sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any `RUN`, `CMD` and `ENTRYPOINT` instructions that follow it in the `Dockerfile`.

```dockerfile
USER patrick
```

### WORKDIR

The `WORKDIR` instruction sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the `Dockerfile`. If the `WORKDIR` doesn’t exist, it will be created even if it’s not used in any subsequent `Dockerfile` instruction.

The `WORKDIR` instruction can be used multiple times in a `Dockerfile`. If a relative path is provided, it will be relative to the path of the previous `WORKDIR` instruction. For example:

```dockerfile
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd # should be /a/b/c
```

```dockerfile
ENV DIRPATH /path
WORKDIR $DIRPATH/app
RUN pwd # should be /path/app
```

### ARG

The `ARG` instruction defines a variable that users can pass at build-time to the builder with the docker build command using the `--build-arg <varname>=<value>` flag. If a user specifies a build argument that was not defined in the `Dockerfile`, the build outputs a warning.

`Dockerfile` may include one or more `ARG` instructions. For example, the following is a valid Dockerfile:

```dockerfile
FROM busybox
ARG user
ARG buildno

RUN echo $user
```

```bash
docker build --build-arg user=what_user .
```

### HEALTHCHECK

The `HEALTHCHECK` instruction has two forms:
* `HEALTHCHECK [OPTIONS] CMD command` (check container health by running a command inside the container)
* `HEALTHCHECK NONE` (disable any healthcheck inherited from the base image)

The `HEALTHCHECK` instruction tells Docker how to test a container to check that it is still working. When a container has a healthcheck specified, it has a health status in addition to its normal status. This status is initially `starting`. Whenever a health check passes, it becomes `healthy` (whatever state it was previously in). After a certain number of consecutive failures, it becomes `unhealthy`.

```dockerfile
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```


Using Dockerfiles
-----------------

Also we can use a Dockerfile to build a new image:

```bash
# Create App Folder
$ mkdir app
```

Then Create Dockerfile to Install PHP stuff `app/Dockerfile`.

```dockerfile
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

```dockerfile
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

```dockerfile
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

```dockerfile
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

```dockerfile
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


Docker Compose
--------------

### Installation

To Install docker compose, run the following command:

```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

$ docker-compose --version
docker-compose version 1.21.2, build a133471
```

### Getting Started.

Let's create a simple python app running with two containers.

```bash
$ mkdir app
```

Create `app/app.py`, `app/requirements.txt`, `app/Dockerfile` and `app/docker-compose.yml`.

```bash
## app/app.py

import time

import redis
from flask import Flask


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    file = open("testfile.txt","w")
    file.write('Hello World! I have been seen {} times.\n'.format(count))
    file.close()
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

```bash
## app/requirements.txt

flask
redis
```

```dockerfile
## app/Dockerfile

FROM python:3.4-alpine
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

```yaml
## app/docker-compose.yml

version: '3'

services:
    web:
        build: .
        ports:
            - "5000:5000"
        volumes:
            - .:/app
    redis:
        image: "redis:alpine"
```

Now Build and run your app with Compose.

```bash
$ cd app

$ docker-compose run web env
Creating network "app_default" with the default driver
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=a50e74216d8d
TERM=xterm
LANG=C.UTF-8
GPG_KEY=97FC712E4C024BBEA48A61ED3A5CA953F73C700D
PYTHON_VERSION=3.4.8
PYTHON_PIP_VERSION=10.0.1
HOME=/root

$ docker-compose run redis env
HOSTNAME=fc45a291fcb0
SHLVL=1
HOME=/root
REDIS_DOWNLOAD_SHA=1db67435a704f8d18aec9b9637b373c34aa233d65b6e174bdac4c1b161f38ca4
TERM=xterm
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-4.0.10.tar.gz
REDIS_VERSION=4.0.10
PWD=/data

$ docker-compose up -d
$ docker ps
$ docker-compose ps

# Go to http://fqdn:5000
# file response.txt should appear and its content change on page refresh

# Stop the applications
$ docker-compose stop

# Restart the applications
$ docker-compose restart

# Start the applications
$ docker-compose start

# Remove containers entirely
$ docker-compose down --volumes
```


Compose file Version 3 
----------------------

The Compose file is a YAML file defining `services`, `networks` and `volumes`. The default path for a Compose file is `./docker-compose.yml`.

A service definition contains configuration that is applied to each container started for that service, much like passing command-line parameters to `docker container create`. Likewise, network and volume definitions are analogous to `docker network create` and `docker volume create`

As with `docker container create`, options specified in the `Dockerfile`, such as `CMD`, `EXPOSE`, `VOLUME`, `ENV`, are respected by default - you don’t need to specify them again in `docker-compose.yml`.

Here is the configuration options supported by a service definition in version 3.

### BUILD

Configuration options that are applied at build time.


```yaml
version: '3'

services:
    webapp:
        build: ./dir # it will use the Dockerfile inside ./dir
```

```yaml
version: '3'

services:
    webapp:
        build:
            context: ./dir  # Either a path to a directory containing a Dockerfile, or a url to a git repository.
                            # When the value supplied is a relative path, it is interpreted as relative to the location of the Compose file. 
                            # This directory is also the build context that is sent to the Docker daemon.
            dockerfile: Dockerfile-alternate    # Compose uses an alternate file to build with. A build path must also be specified
        args:
            buildno: 1  # Add build arguments, which are environment variables accessible only during the build process.
                        # But we need to specify the arguments in your Dockerfile
            gitcommithash: "23442...."
```

```yaml
version: '3'

services:
    webapp:
        build:
            context: . # Will use Dockerfile on the current directory as image
            args:
                buildno: 1
                gitcommithash: cdc3b19
```

```Dockerfile
# Dockerfile-alternate file 

ARG buildno
ARG gitcommithash

RUN echo "Build number: $buildno"
RUN echo "Based on commit: $gitcommithash"

```

**Please note that The docker stack command accepts only pre-built images.**


### CACHE_FROM

This option is new in v3.2. A list of images that the engine uses for cache resolution.

```yaml
version: '3'

services:
    webapp:
        build:
            context: .
            cache_from:
                - alpine:latest
                - corp/web_app:3.14
```


### LABELS

This option is new in v3.3. Add metadata to the resulting image using Docker labels. You can use either an array or a dictionary.
It’s recommended that you use reverse-DNS notation to prevent your labels from conflicting with those used by other software.

```yaml

version: '3'

services:
    webapp:
        build:
            context: .
            labels:
                com.example.description: "Accounting webapp"
                com.example.department: "Finance"
                com.example.label-with-empty-value: ""
```
```yaml
version: '3'

services:
    webapp:
        build:
            context: .
            labels:
                - "com.example.description=Accounting webapp"
                - "com.example.department=Finance"
                - "com.example.label-with-empty-value"
```


### SHM_SIZE

Set the size of the `/dev/shm` partition for this build’s containers. Specify as an integer value representing the number of bytes or as a string expressing a byte value.

```yaml
version: '3'

services:
    webapp:
        build:
            context: .
            shm_size: '2gb'
``` 
```yaml
version: '3'

services:
    webapp:
        build:
            context: .
            shm_size: 10000000
```


### IMAGE

Specify the image to start the container from. Can either be a `repository/tag` or a `partial image ID`.

```yaml
image: redis
image: ubuntu:14.04
image: tutum/influxdb
image: example-registry.com:4000/postgresql
image: a4bc65fd
```

```yaml
version: '3'

services:
    webapp:
        image: ubuntu:14.04
```

If the image does not exist, Compose attempts to pull it, unless you have also specified build, in which case it builds it using the specified options and tags it with the specified tag.


### COMMAND

Override the default command.

```yaml
version: '3'

services:
    webapp:
        image: ubuntu:14.04
        command: bundle exec thin -p 3000
```

The command can also be a list, in a manner similar to dockerfile:

```yaml
version: '3'

services:
    webapp:
        image: ubuntu:14.04
        command: ["bundle", "exec", "thin", "-p", "3000"]
```


### CONFIGS

Grant access to configs on a per-service basis using the per-service configs configuration.

The following example uses the short syntax to grant the redis service access to the `my_config` and `my_other_config` configs. The value of `my_config` is set to the contents of the file `./my_config.txt`, and `my_other_config` is defined as an external resource, which means that it has already been defined in Docker, either by running the `docker config create` command or by another stack deployment. If the external config does not exist, the stack deployment fails with a `config not found error`.

```yaml
version: "3.3"
services:
    redis:
        image: redis:latest
        deploy:
            replicas: 1
        configs:
            - my_config
            - my_other_config
configs:
    my_config:
        file: ./my_config.txt
    my_other_config:
        external: true
```

To work with configs through docker commands

```bash
docker config create
docker config inspect
docker config ls
docker config rm
```

a simple example to attach config to redis container

```bash
$ echo "This is a config" | docker config create my-config -


$ docker service create --name redis --config my-config redis:alpine


$ docker service ps redis

ID            NAME     IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
bkna6bpn8r1a  redis.1  redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago  


$ docker ps --filter name=redis -q

5cb1c2348a59

$ docker container exec $(docker ps --filter name=redis -q) ls -l /my-config

-r--r--r--    1 root     root            12 Jun  5 20:49 my-config                                                     

$ docker container exec $(docker ps --filter name=redis -q) cat /my-config

This is a config


$ docker config ls

ID                          NAME                CREATED             UPDATED
fzwcfuqjkvo5foqu7ts7ls578   hello               31 minutes ago      31 minutes ago


$ docker config rm my-config

Error response from daemon: rpc error: code = 3 desc = config 'my-config' is
in use by the following service: redis


$ docker service update --config-rm my-config redis


$ docker container exec -it $(docker ps --filter name=redis -q) cat /my-config

cat: can't open '/my-config': No such file or directory


$ docker service rm redis


$ docker config rm my-config
```

The following example sets the name of `my_config` to `redis_config` within the container, sets the mode to `0440` (group-readable) and sets the user and group to `103`. The redis service does not have access to the `my_other_config` config.

```yaml
version: "3.3"
services:
    redis:
        image: redis:latest
        deploy:
            replicas: 1
        configs:
            - source: my_config
            target: /redis_config
            uid: '103'
            gid: '103'
            mode: 0440
configs:
    my_config:
        file: ./my_config.txt
    my_other_config:
        external: true
```

Configs cannot be writable because they are mounted in a temporary filesystem, so if you set the writable bit, it is ignored.

You can grant a service access to multiple configs and you can mix long and short syntax. Defining a config does not imply granting a service access to it.


### CONTAINER_NAME

Specify a custom container name, rather than a generated default name.

```yaml
version: "3.3"
services:
    redis:
        image: redis:latest
        container_name: my-redis-container
```

Because Docker container names must be unique, you cannot scale a service beyond 1 container if you have specified a custom name. Attempting to do so results in an error.

This option is ignored when deploying a stack in swarm mode with a (version 3) Compose file.


### DEPLOY

Specify configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with docker stack deploy, and is ignored by `docker-compose up` and `docker-compose run`

```yaml
version: '3'

services:
    redis:
        image: redis:alpine
        deploy:
            replicas: 6
            update_config:
                parallelism: 2
                delay: 10s
            restart_policy:
                condition: on-failure
```


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
