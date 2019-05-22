ELK Stack
=========

Installation
```
$ apt-get update
$ wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
$ sudo apt-get install apt-transport-https
$ echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

// Elasticsearch
$ sudo apt-get update && sudo apt-get install elasticsearch
$ sudo /bin/systemctl daemon-reload
$ sudo /bin/systemctl enable elasticsearch.service
$ sudo systemctl start elasticsearch.service
$ sudo systemctl stop elasticsearch.service

// Kibana
$ sudo apt-get update && sudo apt-get install kibana
$ sudo /bin/systemctl daemon-reload
$ sudo /bin/systemctl enable kibana.service
$ sudo systemctl start kibana.service
$ sudo systemctl stop kibana.service
```
