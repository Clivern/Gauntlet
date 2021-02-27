Cassandra for Developers
========================

### Getting Started

Install Docker and docker-compose

```bash
$ apt-get update
$ apt install docker.io
$ systemctl enable docker
$ apt install docker-compose
```

Create docker-compose file for cassandra cluster

```yaml
version: '3'

services:
  n1:
    image: 'cassandra:4.0'
    networks:
      - cluster

  n2:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment: CASSANDRA_SEEDS=n1
    depends_on:
      - n1

  n3:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment: CASSANDRA_SEEDS=n1
    depends_on:
      - n1

networks:
  cluster: null

```

Run Node 1

```bash
$ docker-compose up -d n1
$ docker ps

$ docker-compose exec n1 nodetool help
$ docker-compose exec n1 nodetool status
$ docker-compose exec n1 nodetool ring
```

Run Node 2

```
$ docker-compose up -d n2
$ docker ps

$ docker-compose exec n2 nodetool status
$ docker-compose exec n2 nodetool ring
```

Run Node 3

```
$ docker-compose up -d n3
$ docker ps
$ docker-compose exec n3 nodetool status
$ docker-compose exec n3 nodetool ring
```
