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
