## Clickhouse Graphouse Integration


### Install ClickHouse:

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4    # optional
echo "deb http://repo.yandex.ru/clickhouse/deb/stable/ main/" | sudo tee /etc/apt/sources.list.d/clickhouse.list
sudo apt-get update
sudo apt-get install -y clickhouse-server clickhouse-client
sudo service clickhouse-server start
clickhouse-client
```

### Install Graphouse:

### Connect ClickHouse & Graphouse:
