### Setup a Highly Available Cassandra Cluster With HAProxy

Assuming we have the following servers

```
cas01          10.10.10.10     1.1.1.1
cas02          11.11.11.11     2.2.2.2
cas03          12.12.12.12     3.3.3.3

hprox          13.13.13.13     4.4.4.4
```

Install Cassandra on the first three servers

```zsh
$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install openjdk-8-jdk apt-transport-https -y
$ java -version
$ sudo sh -c 'echo "deb http://www.apache.org/dist/cassandra/debian 40x main" > /etc/apt/sources.list.d/cassandra.list'
$ wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
$ sudo apt update
$ sudo apt install cassandra
$ sudo systemctl enable cassandra
```

Adjust the `/etc/cassandra/cassandra.yaml` on the first three servers.

```yaml
. . .

cluster_name: 'ProdCassandraCluster'

. . .

seed_provider:
  - class_name: org.apache.cassandra.locator.SimpleSeedProvider
    parameters:
         - seeds: "1.1.1.1:7000,2.2.2.2:7000,3.3.3.3:7000"

. . .

listen_address: node_private_ip

. . .

rpc_address: node_private_ip

. . .

endpoint_snitch: GossipingPropertyFileSnitch

. . .

auto_bootstrap: false
```

After adjusting the three cassandra nodes, stop the three, delete system files and start them again

```zsh
$ service cassandra stop
$ sudo rm -rf /var/lib/cassandra/data/system/*
$ service cassandra start
```

Edit HAProxy config file `/etc/haproxy/haproxy.cfg` and restart afterwards.

```cfg
defaults
	mode	tcp

frontend stats
    bind *:8404
    stats enable
    mode http
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST

frontend cassandra-cql
    description "Cassandra CQL"
    bind *:9042
    mode tcp
    option tcplog
    default_backend cassandra-cql

backend cassandra-cql
    description "Cassandra CQL"
    balance leastconn
    mode tcp
    server 1.1.1.1 1.1.1.1:9042 check
    server 2.2.2.2 2.2.2.2:9042 check
    server 3.3.3.3 3.3.3.3:9042 check
```

You should be able to reach cassandra nodes through HAProxy

```zsh
$ cqlsh 13.13.13.13 9042
```

HAProxy dashboard will be available via this link http://13.13.13.13:8404/stats
