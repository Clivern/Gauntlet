Cassandra for Developers
========================

Apache Cassandra is a free and open-source, distributed, NoSQL database management system designed to handle large amounts of data across many servers, providing high availability with no single point of failure. Cassandra offers robust support for clusters spanning multiple datacenters, with asynchronous masterless replication allowing low latency operations for all clients.

### Gettings Started

Install Docker and docker-compose for testing purposes

```bash
$ apt-get update
$ apt install docker.io
$ systemctl enable docker
$ apt install docker-compose
```


### Setup Multi Node Cluster

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
    environment:
        - CASSANDRA_SEEDS=n1
    depends_on:
      - n1

  n3:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment:
        - CASSANDRA_SEEDS=n1
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
$ docker-compose exec n1 more /etc/cassandra/cassandra.yaml
```

Run Node 2

```
$ docker-compose up -d n2
$ docker ps

$ docker-compose exec n2 nodetool status
$ docker-compose exec n2 nodetool ring
$ docker-compose exec n2 more /etc/cassandra/cassandra.yaml
```

Run Node 3

```
$ docker-compose up -d n3
$ docker ps
$ docker-compose exec n3 nodetool status
$ docker-compose exec n3 nodetool ring
$ docker-compose exec n3 more /etc/cassandra/cassandra.yaml
```


### Setup Multi DC Cluster

Create docker-compose file for cassandra cluster

```
version: '3'

services:
  n1:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment:
        - CASSANDRA_SEEDS=n1
        - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
        - CASSANDRA_DC=DC1
        - CASSANDRA_RACK=RAC1
  n2:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment:
        - CASSANDRA_SEEDS=n1
        - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
        - CASSANDRA_DC=DC1
        - CASSANDRA_RACK=RAC2
    depends_on:
      - n1

  n3:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment:
        - CASSANDRA_SEEDS=n1
        - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
        - CASSANDRA_DC=DC2
        - CASSANDRA_RACK=RAC1
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
$ docker-compose exec n1 more /etc/cassandra/cassandra.yaml
$ docker-compose exec n1 more /etc/cassandra/cassandra-rackdc.properties
```

Run Node 2

```
$ docker-compose up -d n2
$ docker ps

$ docker-compose exec n2 nodetool status
$ docker-compose exec n2 nodetool ring
$ docker-compose exec n2 more /etc/cassandra/cassandra.yaml
$ docker-compose exec n2 more /etc/cassandra/cassandra-rackdc.properties
```

Run Node 3

```
$ docker-compose up -d n3
$ docker ps
$ docker-compose exec n3 nodetool status
$ docker-compose exec n3 nodetool ring
$ docker-compose exec n3 more /etc/cassandra/cassandra.yaml
$ docker-compose exec n3 more /etc/cassandra/cassandra-rackdc.properties
```


### Replication

`SimpleStrategy`: this is the best used in development environment or single data center clusters

```sql
CREATE KEYSPACE IF NOT EXISTS clivern WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
```

Here we are asking cassandra to store three copies for all the partitions in all the tables in `clivern` keyspace.

Let's create a `docker-compose.yml` file for multi-node cluster

```yaml
version: '3'

services:
  n1:
    build: .
    image: cassandra-with-cqlshrc
    networks:
      - cluster

  n2:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment:
        - CASSANDRA_SEEDS=n1
    depends_on:
      - n1

  n3:
    image: 'cassandra:4.0'
    networks:
      - cluster
    environment:
        - CASSANDRA_SEEDS=n1
    depends_on:
      - n1

networks:
  cluster: null
```

and create `Dockerfile`

```
FROM cassandra:4.0

COPY cqlshrc /root/.cqlshrc
```

and create `cqlshrc` file

```config
[connection]

;; a timeout in seconds for opening a new connection
timeout = 60

;; a timeout in seconds to execute queries
request_timeout = 60
```

Bring up the cluster node and wait

```bash
$ docker-compose up -d
```

Get cluster nodes status

```bash
$ docker-compose exec n1 nodetool status
```

Use `cqlsh` command line tool

```bash
$ docker-compose exec n1 cqlsh
# Create the keyspace
>> CREATE KEYSPACE IF NOT EXISTS clivern WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

$ docker-compose exec n1 nodetool describering clivern
$ docker-compose exec n3 nodetool status clivern


$ docker-compose exec n1 cqlsh
>> drop keyspace clivern;
>> CREATE KEYSPACE IF NOT EXISTS clivern WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
```


`NetworkTopologyStrategy`: this is the best used in production with multi datacenter clusters

```sql
CREATE KEYSPACE IF NOT EXISTS clivern WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'DC1' : 3, 'DC2' : 1 };
```

Here we storing four copies of the data, 3 copies in DC1 and 1 copy in DC2. You can do something similar to what i did in `SimpleStrategy`


### Consistency

`Consistency level` determines how many nodes in the replica must respond for the coordinator node to successfully process a non-lightweight transaction. The consistency level defaults to ONE for all write and read operations.

For a list of all supported `Write Consistency Levels`, please check this table https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html#Writeconsistencylevels

For a list of all supported `Read Consistency Levels`, please check this table https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html#Readconsistencylevels

Please note that:

- `Hinted Handoff`:  On occasion, a node becomes unresponsive while data is being written. a hinted handoff inherently allows Cassandra to continue performing the same number of writes even when the cluster is operating at reduced capacity. for more info, please check this guide https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/operations/opsRepairNodesHintedHandoff.html.

- `Read Repair`: Read repair improves consistency in a Cassandra cluster with every read request. for more info, please check this guide https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/operations/opsRepairNodesReadRepair.html


### Introduction to CQL

Let’s create a `docker-compose.yml` file for a single node

```
version: '3'

services:
  n1:
    build: .
    image: cassandra-with-cqlshrc
    networks:
      - cluster

networks:
  cluster: null
```

and create `Dockerfile`

```
FROM cassandra:4.0

COPY cqlshrc /root/.cqlshrc
```

and create `cqlshrc` file

```
[connection]

;; a timeout in seconds for opening a new connection
timeout = 60

;; a timeout in seconds to execute queries
request_timeout = 60
Bring up the cluster node and wait
```

Bring up the cluster node and wait

```
$ docker-compose up -d
```

Get cluster nodes status

```
$ docker-compose exec n1 nodetool status
```

Use `cqlsh` command line tool

```
$ docker-compose exec n1 cqlsh

cqlsh> create keyspace clivern with replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
cqlsh> use clivern;
```

To create a table

```
cqlsh:clivern> create table if not exists user (id uuid primary key, username varchar);
cqlsh:clivern> alter table user add firstname varchar;
cqlsh:clivern> desc table user;

CREATE TABLE clivern.user (
    id uuid PRIMARY KEY,
    firstname text,
    username text
) WITH additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND cdc = false
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND extensions = {}
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';
```

To insert rows

```
cqlsh:clivern> insert into user (id, username) values (92d99616-a899-487a-852c-40bee1d9b6eb, 'joe');
cqlsh:clivern> insert into user (id, username) values (92d9962e-9710-4c63-81c7-fc7fb31b3162, 'doe');
```

To select rows

```
cqlsh:clivern> select * from user where id = 92d99616-a899-487a-852c-40bee1d9b6eb limit 1;

cqlsh:clivern> select * from user where username = 'joe' limit 1;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"

cqlsh:clivern> select * from user where username = 'joe' ALLOW FILTERING;
```

To update rows

```
cqlsh:clivern> update user set firstname = 'Joe' where id = 92d99616-a899-487a-852c-40bee1d9b6eb;

cqlsh:clivern> select * from user where id = 92d99616-a899-487a-852c-40bee1d9b6eb limit 1;

 id                                   | firstname | username
--------------------------------------+-----------+----------
 92d99616-a899-487a-852c-40bee1d9b6eb |       Joe |      joe
```

To delete rows

```
cqlsh:clivern> delete from user where id = 92d99616-a899-487a-852c-40bee1d9b6eb;
cqlsh:clivern> select * from user where id = 92d99616-a899-487a-852c-40bee1d9b6eb limit 1;

 id | firstname | username
----+-----------+----------

(0 rows)
```


### Multi-row Partitions


### Complex Data Types


### Making the Most of Cassandra
