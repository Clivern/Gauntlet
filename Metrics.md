Metrics
=======

Graphite
--------

### Install With Docker

```console
docker run -d\
 --name graphite\
 --restart=always\
 -p 80:80\
 -p 2003-2004:2003-2004\
 -p 2023-2024:2023-2024\
 -p 8125:8125/udp\
 -p 8126:8126\
 graphiteapp/graphite-statsd
```

### Push Some Data

```python
#!/usr/bin/env python

import socket
import time


CARBON_SERVER = 'xxx.yyy.z.kkk'
CARBON_PORT = 2003
DELAY = 3  # secs


def send_msg(message):
    print 'sending message:\n%s' % message
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message)
    sock.close()


if __name__ == '__main__':
    i = 1
    j = 1
    k = 1
    while True:
        i += 1
        j += 2
        k += 3
        timestamp = int(time.time())
        lines = [
            'parent1.parent2.child %s %d' % (i, timestamp),
            'parent1.parent2.child %s %d' % (j, timestamp),
            'parent1.parent2.child %s %d' % (k, timestamp)
        ]
        message = '\n'.join(lines) + '\n'
        send_msg(message)
        time.sleep(DELAY)
```

[Check the API Docs.](http://graphite-api.readthedocs.io/en/latest/api.html)


Prometheus
----------

### Install on Linux

```console
wget https://github.com/prometheus/prometheus/releases/download/v2.3.2/prometheus-2.3.2.linux-amd64.tar.gz

# Should Be ~> 351931fe9bb252849b7d37183099047fbe6d7b79dcba013fb6ae19cc1bbd8552
sha256sum prometheus-*.tar.gz

tar xvfz prometheus-*.tar.gz
rm prometheus-*.tar.gz
cd prometheus-*
./prometheus --help
```

Create a basic config file to scrape prometheus metrics every 15 seconds.

```
# prometheus.yml
global:
  scrape_interval:     15s
  evaluation_interval: 15s

rule_files:
  # - "first.rules"
  # - "second.rules"

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']
```

Start prometheus server.

```console
./prometheus --config.file=prometheus.yml
```

### Install With Docker

Bind-mount your `prometheus.yml` from the host by running

```console
docker run -p 9090:9090 -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

Or use an additional volume for the config

```console
docker run -p 9090:9090 -v /prometheus-data prom/prometheus --config.file=/prometheus-data/prometheus.yml
```


### Getting Started

we can add `localhost:5000` to be scraped and run new app with [flask](http://flask.pocoo.org/) listening on port `5000`:

```console
pip install Flask
```

```python
# hello.py

from flask import Flask
app = Flask(__name__)

@app.route("/metrics")
def hello():
    return 'item_to_trace 46'
````

```console
FLASK_APP=hello.py flask run --host=0.0.0.0
```

Grafana
-------

### Install With Docker

```console
docker run \
  -d \
  -p 3000:3000 \
  --name=grafana \
  -e "GF_SERVER_ROOT_URL=http://grafana.example.com" \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  grafana/grafana
```

[Check the API Docs.](http://docs.grafana.org/)
