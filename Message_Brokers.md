Message Brokers 
===============

Working With Apache Kafka
-------------------------
```bash
# Install Java
sudo add-apt-repository ppa:webupd8team/java
sudo apt update; sudo apt install oracle-java8-installer
sudo apt install oracle-java8-set-default

# Install Kafka
wget http://apache.cs.uu.nl/kafka/1.1.0/kafka_2.11-1.1.0.tgz
tar -xzf kafka_2.11-1.1.0.tgz
cd kafka_2.11-1.1.0
nohup bin/zookeeper-server-start.sh config/zookeeper.properties > /dev/null 2>&1 &
sleep 9
nohup bin/kafka-server-start.sh config/server.properties > /dev/null 2>&1 &

# Let's create a topic named "test" with a single partition and only one replica:
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
# We can now see that topic if we run the list topic command
bin/kafka-topics.sh --list --zookeeper localhost:2181

# Send some messages
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test

# Start a consumer
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```
