Load Balancing
==============

MySQL Master Slave Replication:
-------------------------------

We need to Create at least 2 Servers:

* Mater Server `178.128.252.199`
* Slave Server `178.128.252.201`

### Configure The Master

```console
ssh root@178.128.252.199
# Install MySQL
sudo apt-get install mysql-server mysql-client

# Config The MySQL Server to be Master
$ nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Set bind address and DB to Replicate
bind-address            = 178.128.252.199
server-id               = 1
log_bin                 = /var/log/mysql/mysql-bin.log
binlog_do_db            = scale

# Restart MySQL
$ sudo service mysql restart

# Create Slave User & Password
$ mysql -u root -p

mysql> GRANT REPLICATION SLAVE ON *.* TO 'slave_user'@'%' IDENTIFIED BY 'password';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)

mysql> USE scale
Database changed

mysql> FLUSH TABLES WITH READ LOCK;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW MASTER STATUS;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      595 | scale        |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)

mysql> QUIT

# Get The State of DB before accepting Changes
$ mysqldump -u root -p --opt scale > scale.sql

# Unlock DB
$ mysql -u root -p

mysql> USE scale;

mysql> UNLOCK TABLES;

mysql> QUIT;
```


### Configure The Slave

```console
ssh root@178.128.252.201

# Install MySQL
sudo apt-get install mysql-server mysql-client

# Config The MySQL Server to be a Slave
$ nano /etc/mysql/mysql.conf.d/mysqld.cnf

server-id               = 2
log_bin                 = /var/log/mysql/mysql-bin.log
binlog_do_db            = scale

$ sudo service mysql restart

$ mysql -u root -p

mysql> CREATE DATABASE scale;

mysql> QUIT

$ mysql -u root -p scale < scale.sql

$ mysql -u root -p

mysql> CHANGE MASTER TO MASTER_HOST='178.128.252.199',MASTER_USER='slave_user', MASTER_PASSWORD='password', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=  595;

mysql> START SLAVE;

mysql> SHOW SLAVE STATUS \G
