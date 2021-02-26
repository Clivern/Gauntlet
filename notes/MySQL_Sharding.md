MySQL Sharding
==============

Practice 1
----------
First We have a database with lookup table for username, email & location (`FINAL_ID`) of userdata.

```mysql
- ID
- username
- email
- location
```

We will create an ID that contains the shard ID, the database ID, and where this data is in the table (Primary ID).

```python
FINAL_ID = (SHARD_ID << 46) | (DB_ID << 36) | (PRIMARY_ID << 0)
```

Given this URL `http://www.example.com/user/241294492511762325/`, we will decompose it like the following:

```python
SHARD_ID = (241294492511762325 >> 46) & 0xFFFF = 3429
DB_ID  = (241294492511762325 >> 36) & 0x3FF = 1
PRIMARY_ID = (241294492511762325 >>  0) & 0xFFFFFFFFF = 7075733
```

We expect foreign keys to work as expected because all user data will be on same db and same shard. but we have one problem that we may have a really big lookup table.


References
----------
* [Understanding Database Sharding](https://www.digitalocean.com/community/tutorials/understanding-database-sharding)
