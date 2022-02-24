Jenkins
-------

To Install Jenkins Server

```bash
sudo apt install openjdk-11-jdk
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

To Install Jenkins Node

```bash
apt-get update
sudo apt install openjdk-11-jdk
sudo apt install docker.io
sudo systemctl enable docker
```
