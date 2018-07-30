Celery ~ Distributed Task Queue
===============================

```bash
# Run RabbitMQ Container
docker pull rabbitmq
docker run -d --hostname my-rabbit --name some-rabbit -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 15672:15672 rabbitmq
docker exec some-rabbit rabbitmq-plugins enable rabbitmq_management

# Login at http://localhost:15672/ (or the IP of your docker host)
# using guest/guest
```

```bash
# Run Redis Container
docker run -d --name redis -p 6379:6379 redis
```

### Basic Usage

```python
pip install celery
pip install -U "celery[redis]"
```

```python
# Task.py
from celery import Celery

app = Celery(
    'tasks', 
    backend='redis://x.x.x.x:6379', 
    broker='amqp://guest:guest@x.x.x.x:5672'
)

@app.task
def add(x, y):
    return x + y
```

```bash
~ python

>>> from tasks import add
>>> from celery.result import AsyncResult

>>> add.delay(8, 8)
<AsyncResult: c1bc24dc-fb27-4133-bd16-25230f67eedd>
>>> AsyncResult('c1bc24dc-fb27-4133-bd16-25230f67eedd').state
'SUCCESS'
>>> AsyncResult('c1bc24dc-fb27-4133-bd16-25230f67eedd').status
'SUCCESS'
# To ensure that resources are released from backend
>>> AsyncResult('c1bc24dc-fb27-4133-bd16-25230f67eedd').forget()
```

```bash
# To Run Workers
celery -A tasks worker --loglevel=info -n worker1
celery -A tasks worker --loglevel=info -n worker2
celery -A tasks worker --loglevel=info -n worker3
```
