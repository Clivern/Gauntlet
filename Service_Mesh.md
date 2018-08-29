Consul
------


### Why

Load balancers aren't efficient in a dynamic environment where we scale services up or down. Consul uses a registry to keep a real-time list of services, their location, and their health. Services query the registry to discover the location of upstream services and then connect directly. This allows services to scale up/down and gracefully handle failure.


### Installation

To Install Consul on Ubuntu

```bash
apt-get update
cd /usr/local/bin
wget https://releases.hashicorp.com/consul/1.2.2/consul_1.2.2_linux_amd64.zip
wget https://releases.hashicorp.com/consul/1.2.2/consul_1.2.2_SHA256SUMS
sha256sum consul_1.2.2_linux_amd64.zip
grep "consul_1.2.2_linux_amd64.zip" consul_1.2.2_SHA256SUMS
rm consul_1.2.2_SHA256SUMS
unzip *.zip
rm *.zip

# Refer to https://www.consul.io/docs/agent/options.html#ports for required ports and optional
ufw allow 8300
ufw allow 8301
ufw allow 8302
ufw allow 8400
ufw allow 8500
ufw allow 8600

mkdir /tmp/consul_services
mkdir /tmp/consul
```


#### Run Consul Leader

You need to create a system service for consul `nano /etc/systemd/system/consul.service`

```bash
[Unit]
Description=Consul
Documentation=https://www.consul.io/

[Service]
ExecStart=/usr/local/bin/consul agent -server -bootstrap -data-dir /tmp/consul -bind $LEADER_SERVER_IP_HOST -config-dir /tmp/consul_services -enable-script-checks -datacenter US
ExecReload=/bin/kill -HUP $MAINPID
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

Then

```bash
systemctl daemon-reload
systemctl start consul.service
```

#### Run Consul Web Client

You need to create a system service for consul `nano /etc/systemd/system/consul.service`

```bash
[Unit]
Description=Consul
Documentation=https://www.consul.io/

[Service]
ExecStart=/usr/local/bin/consul agent -data-dir /tmp/consul -ui -client $CLIENT_SERVER_IP_HOST -join $LEADER_SERVER_IP_HOST -enable-script-checks -datacenter US
ExecReload=/bin/kill -HUP $MAINPID
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

Then

```bash
systemctl daemon-reload
systemctl start consul.service
```


#### Run Consul Client

You need to create a system service for consul `nano /etc/systemd/system/consul.service`

```bash
[Unit]
Description=Consul
Documentation=https://www.consul.io/

[Service]
ExecStart=/usr/local/bin/consul agent -server -data-dir /tmp/consul -bind $NORMAL_SERVER_IP_HOST -join $LEADER_SERVER_IP_HOST -config-dir /tmp/consul_services -enable-script-checks -datacenter US
ExecReload=/bin/kill -HUP $MAINPID
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

Then

```bash
systemctl daemon-reload
systemctl start consul.service
```


#### Service Definition

Just create a [web services definition](https://www.consul.io/docs/agent/services.html) `web.json` on `/tmp/consul_services` directory

```json
{
   "services":[
      {
         "name":"serviceA",
         "port":5000,
         "check":{
            "args":[
               "curl",
               "localhost:5000"
            ],
            "interval":"3s"
         }
      },
      {
         "name":"serviceB",
         "port":8000,
         "check":{
            "args":[
               "curl",
               "localhost:8000"
            ],
            "interval":"3s"
         }
      }
   ]
}
```


### Working With Consul Cluster

Services should interact on realtime with consul cluster to register, unregister itself and enable & disable maintenance mode. So if we have microservice `Mocha` running on server x.x.x.x on port 5000 and Consul already running on that server. Service can simply do the following to join the cluster and also to leave on failure.

```bash
# Register A Service (Mocha) 
curl -X PUT \
    -d '{
        "ID": "mocha",
        "Name": "Mocha",
        "Port": 5000,
        "Address": "x.x.x.x",
        "Tags": 
            [
                "primary",
                "v1"
            ],
        "Check": {
            "Args": [
                "curl",
                "http://localhost:5000"
            ],
            "Interval": "10s"
        }
    }' "http://localhost:8500/v1/agent/service/register"

# Enable Maintenance Mode
curl -X PUT \
    -d '' "http://localhost:8500/v1/agent/service/maintenance/mocha?enable=true&reason=Something+goes+wrong!"

# Disable Maintenance Mode
curl -X PUT \
     -d '' "http://localhost:8500/v1/agent/service/maintenance/mocha?enable=false&reason=I+am+back!"

# Unregister A Service (Mocha)
curl -X PUT \
    -d '' "http://localhost:8500/v1/agent/service/deregister/mocha"
```


### Health Endpoints

For a complete guide, [go here](https://www.consul.io/api/health.html) but for the important stuff, check the following:

```bash
# Get All Healthy Services on Consul Cluster
curl -X GET \
    http://localhost:8500/v1/health/state/passing | python -m json.tool


# List Healthy Checks for a Service (Mocha)
curl -X GET \
    http://localhost:8500/v1/health/checks/mocha | python -m json.tool


# Get Healthy Services with nodes data, This can be used for dynamic load balancing
curl -X GET \
    http://localhost:8500/v1/health/service/mocha?passing=true | python -m json.tool
[
    {
        "Checks": [

        ],
        "Node": {

        },
        "Service": {
            "Address": "x.x.x.x",
            "Connect": {
                "Native": false,
                "Proxy": null
            },
            "CreateIndex": 3121,
            "EnableTagOverride": false,
            "ID": "mocha",
            "Meta": null,
            "ModifyIndex": 3121,
            "Port": 5000,
            "ProxyDestination": "",
            "Service": "Mocha",
            "Tags": [
                "primary",
                "v1"
            ]
        }
    },
    {
        "Checks": [

        ],
        "Node": {
 
        },
        "Service": {
            "Address": "y.y.y.y",
            "Connect": {
                "Native": false,
                "Proxy": null
            },
            "CreateIndex": 3318,
            "EnableTagOverride": false,
            "ID": "mocha",
            "Meta": null,
            "ModifyIndex": 3318,
            "Port": 5000,
            "ProxyDestination": "",
            "Service": "Mocha",
            "Tags": [
                "secondary",
                "v1"
            ]
        }
    }
]
```


#### KV Store Endpoints

```bash
# Create & Update Item
curl -X PUT \
    -d '2days' http://localhost:8500/v1/kv/mocha_flush


# Get Item
curl -X GET \
     http://localhost:8500/v1/kv/mocha_flush | python -m json.tool
[
    {
        "CreateIndex": 3827,
        "Flags": 0,
        "Key": "mocha_flush",
        "LockIndex": 0,
        "ModifyIndex": 3827, # base64-encoded blob
        "Value": "MjNkYXlz"
    }
]

# Delete Item
curl -X DELETE \
    http://localhost:8500/v1/kv/mocha_flush
```
