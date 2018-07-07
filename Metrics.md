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

[Check the API Docs.](http://docs.grafana.org/)
