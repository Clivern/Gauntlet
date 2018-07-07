Metrics
=======

Graphite
--------

### Install With Docker

```bash
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

[Check the API docs here.](http://graphite-api.readthedocs.io/en/latest/api.html)

Grafana
-------

### Install With Docker

```bash
docker run \
  -d \
  -p 3000:3000 \
  --name=grafana \
  -e "GF_SERVER_ROOT_URL=http://grafana.example.com" \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  grafana/grafana
```

[Check the API docs here.](http://docs.grafana.org/)
