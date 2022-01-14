## Observability Stack

### Grafana

To install grafana, use the following commands on ubunut 20.04:

```zsh
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

sudo apt-get update
sudo apt-get install grafana
```

### Grafana Loki

To install grafana loki, use the following commands on ubunut 20.04:
