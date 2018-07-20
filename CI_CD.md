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
