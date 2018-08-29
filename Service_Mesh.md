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
# Register Service
curl -X PUT -H "Content-Type: application/json" -d '{"ID": "mocha","Name": "Mocha","Port": 5000, "Address": "x.x.x.x","Tags": ["primary","v1"],"Check": {"Args": ["curl","http://localhost:5000"],"Interval": "10s"}}' "http://localhost:8500/v1/agent/service/register"

# Enable Maintenance Mode
curl -X PUT -d '' "http://localhost:8500/v1/agent/service/maintenance/mocha?enable=true&reason=Something+goes+wrong!"

# Disable Maintenance Mode
curl -X PUT -d '' "http://localhost:8500/v1/agent/service/maintenance/mocha?enable=false&reason=I+am+back!"

# Unregister Service
curl -X PUT -d '' "http://localhost:8500/v1/agent/service/deregister/mocha"
```
