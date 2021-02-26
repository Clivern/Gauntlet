<p align="center">
    <img alt="Nomad" src="https://s3.amazonaws.com/hashicorp-marketing-web-assets/brand/Nomad_VerticalLogo_FullColor.r1x_p8YHag.svg" width="120" />
</p>


### Basic Setup

- Download nomad binary & make it executable:

```
$ wget https://releases.hashicorp.com/nomad/0.12.3/nomad_0.12.3_linux_amd64.zip
$ unzip nomad_0.12.3_linux_amd64.zip
$ mv nomad /usr/local/bin/
```

- Create configs directory & data directory:

```
$ sudo mkdir --parents /opt/nomad
$ sudo mkdir --parents /opt/data
$ sudo mkdir --parents /etc/nomad.d
$ sudo chmod 700 /etc/nomad.d
$ sudo chmod 700 /opt/data

$ sudo touch /etc/nomad.d/nomad.hcl
$ sudo touch /etc/nomad.d/server.hcl
$ sudo touch /etc/nomad.d/client.hcl
```

- Add this configuration to the `/etc/nomad.d/nomad.hcl` configuration file

```
datacenter = "dc1"
data_dir = "/opt/nomad"
```

- Add this configuration to the `/etc/nomad.d/client.hcl` configuration file

```hcl
client {
  enabled = true

  host_volume "redis_data" {
    path      = "/opt/data"
    read_only = false
  }
}
```

- Add this configuration to the `/etc/nomad.d/server.hcl` configuration file

```hcl
acl {
  enabled = true
}
server {
  enabled = true
  bootstrap_expect = 3
}
```

- Create a nomad service file

```
sudo touch /etc/systemd/system/nomad.service
```

- Add this configuration to the nomad service file

```
[Unit]
Description=Nomad
Documentation=https://nomadproject.io/docs/
Wants=network-online.target
After=network-online.target

[Service]
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/local/bin/nomad agent -config /etc/nomad.d
KillMode=process
KillSignal=SIGINT
LimitNOFILE=infinity
LimitNPROC=infinity
Restart=on-failure
RestartSec=2
StartLimitBurst=3
StartLimitIntervalSec=10
TasksMax=infinity

[Install]
WantedBy=multi-user.target
```

- Start nomad

```
sudo systemctl enable nomad
sudo systemctl start nomad
sudo systemctl status nomad
```

- Genertal ACL secrets

```
$ nomad acl bootstrap
Accessor ID  = 57ae3a71-037a-a34f-1a08-dc4385995807
Secret ID    = c5bb4122-9393-fb86-b3e6-91aa62697e4f
Name         = Bootstrap Token
Type         = management
Global       = true
Policies     = n/a
Create Time  = 2020-08-29 22:04:59.419597143 +0000 UTC
Create Index = 10
Modify Index = 10

$ export NOMAD_TOKEN=c5bb4122-9393-fb86-b3e6-91aa62697e4f
```

- Create your first job to deploy a stateless container from the server ui `http://127.0.0.1:4646/ui`

```hcl
job "api" {
  datacenters = ["dc1"]

  group "example" {
    task "server" {
      driver = "docker"

      config {
        image = "hashicorp/http-echo"

        args = [
          "-listen",
          ":5678",
          "-text",
          "hello world",
        ]
      }

      resources {
        network {
          mbits = 10

          port "http" {
            static = "5678"
          }
        }
      }
    }
  }
}
```

- And another one for stateful container

```hcl
job "cache" {
  datacenters = ["dc1"]

  group "redis" {

    volume "redis_data" {
      type      = "host"
      read_only = false
      source    = "redis_data"
    }

    task "redis" {
      driver = "docker"

      volume_mount {
        volume      = "redis_data"
        destination = "/data"
        read_only   = false
      }

      config {
        image = "redis:3.2"
        labels {
          "com.clivern.foo" = "bar"
          "com.clivern.zip" = "zap"
        }
      }

      resources {
        cpu    = 500
        memory = 128
        network {
          mbits = 10
          port "tcp" {
            static = "6379"
          }
        }
      }
    }
  }
}
```


### References

- [Nomad Docs](https://www.nomadproject.io/docs)
- [Learn Nomad](https://learn.hashicorp.com/collections/nomad/get-started)
