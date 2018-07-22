CI/CD Best Practices
====================

Jenkins
-------

### Installation

```bash
# Install Docker
$ apt-get update
$ sudo apt install docker.io
$ sudo systemctl enable docker

# Install Java
$ sudo add-apt-repository ppa:webupd8team/java
$ sudo apt update; sudo apt install oracle-java8-installer
$ sudo apt install oracle-java8-set-default

# Install Jenkins
$ wget http://mirrors.jenkins.io/war-stable/latest/jenkins.war
$ sudo nano /etc/systemd/system/jenkins.service

[Unit]
Description=Jenkins Service
After=syslog.target
[Service]
WorkingDirectory=/root/
SyslogIdentifier=Jenkins
ExecStart=/bin/bash -c "java -jar /root/jenkins.war --httpPort=8080"
User=root
Type=simple
[Install]
WantedBy=multi-user.target


$ systemctl daemon-reload
$ systemctl start jenkins.service
$ systemctl status jenkins.service
```

### Using Docker with Pipeline

Create a Docker Image `Dockerfile`.

```bash
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update

RUN apt-get install -yq \
        php7.2 \
        build-essential \
        openssh-client \
        ca-certificates \
        git \
        php-xdebug \
        php7.2-bcmath \
        php7.2-cli \
        php7.2-curl \
        php7.2-gd \
        php7.2-intl \
        php7.2-mbstring \
        php7.2-mysql \
        php7.2-sqlite3 \
        php7.2-xmlrpc \
        php7.2-xsl \
        php7.2-xml \
        php7.2-zip

RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
    php -r "unlink('composer-setup.php');"

ENV HOME /opt
WORKDIR /opt

CMD ["php", "-a"]
```

Then Build The Image

```bash
docker build -t clivern_php72 .
```

Create a `Jenkinsfile` to do testing using that docker image.

```groovy
pipeline {
  agent {
    docker {
      image 'clivern_php72:latest'
    }
  }
  stages {
    stage('Build') {
      steps {
        sh 'php --version'
      }
    }
    stage('Composer') {
      steps {
        sh 'composer install'
      }
    }
    stage('Test') {
      steps {
        sh './vendor/bin/simple-phpunit'
      }
    }
  }
}
```

Or to use the `Dockerfile` Directly.

```groovy
pipeline {
  agent { dockerfile true }
  stages {
    stage('Build') {
      steps {
        sh 'php --version'
      }
    }
    stage('Testing') {
      steps {
        sh 'make ci'
      }
    }
  }
}
```

For More info, [Please check this guide](https://jenkins.io/doc/book/pipeline/docker/).
