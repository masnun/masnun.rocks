+++
author = ""
date = "2016-11-02T07:07:09+06:00"
description = ""
tags = ["Python", "Django"]
title = "Deploying Django Channels using Daphne"

+++

In one of my <a href="http://masnun.rocks/2016/09/25/introduction-to-django-channels/">earlier post</a>, we 
have seen an overview of how Django Channels work and how it helps us build cool stuff. However, in that post, 
we covered deployment briefly. So here in this post, we shall go over deployment again, with a little more details 
and of course code samples. 

### What do we need? 

For running Django Channels, we would use the following setup: 

* nginx as the proxy
* daphne as the interface server
* redis as the backend 

Let's get started. 

### Setup Redis and Configure App

We need to setup redis if it's not installed already. Here's how to do it on Ubuntu:

```
sudo apt-get install redis-server
```

If we want to use the redis backend, we also need to setup `asgi-redis`. 

```
pip install asgi_redis
```

In your `settings.py` file, make sure you used redis as the backend and input the host properly. 

Here's a demo: 

```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
        "ROUTING": "realtime.routing.channel_routing",
    },
}
```

### Starting Daphne 

If you have installed `channels` from pip, you should have the `daphne` command available already. In the very 
unlikely case you don't have it installed, here's the command: 

```
pip install daphne
```

To run daphne, we use the following command: 

```
daphne -b 0.0.0.0 -p 8001 <app>.asgi:channel_layer
```
Daphne will bind to `0.0.0.0` and use `8001` as the port. 

Here `<app>` is our app name / the module that contains the `asgi.py` file. Please refer to the previous blog post 
to know what we put in the `asgi.py` file. 

We now need to make sure `daphne` is automatically started at system launch and restarted when it crashes. In this 
example, I would stick to my old upstart script. But you would probably want to explore excellent projects like 
`circus` or `supervisor` or at least `systemd`. 

Here's the upstart script I use: 

```
start on runlevel [2345]
stop on runlevel [016]

respawn

script
    cd /home/ubuntu/<app home>
    export DJANGO_SETTINGS_MODULE="<app>.production_settings"
    exec daphne -b 0.0.0.0 -p 8001 <app>.asgi:channel_layer
end script

```

### Running Workers

We need at least one running worker before daphne can start processing requests. To run a worker, we use the 
following command: 

```
python manage.py runworker
```

The `runworker` command spawns one worker with one thread. We should have more than one ideally. It is recommended
to have `n` number of workers where `n` is the number of available cpu cores. 

Here's a simple upstart script to keep the worker running: 

```
start on runlevel [2345]
stop on runlevel [016]

respawn

script
    cd /home/ubuntu/<app home>
    export DJANGO_SETTINGS_MODULE="<app>.production_settings"
    exec python3 manage.py runworker
end script
```

It would be much easier to launch multiple workers if you use supervisord or circus. 

### Nginx Conf 

Finally here's the nginx conf I use. Please note I handle all incoming requests with daphne which is probably 
not ideal. You can keep using `uwsgi` for your existing, non real time parts and only handle the real time part 
with daphne. Since setting up wsgi is popular knowledge, I will just focus on what we need for daphne. 

```
server {
    listen 80;
    client_max_body_size 20M;

    location /static {
       	alias /home/ubuntu/<app home>/static;

    }

    location /media {
        alias /home/ubuntu/<app home>/media;

    }

    location / {


       	    proxy_pass http://0.0.0.0:8001;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;

        }

}
```

We have our daphne server running on port `8001` so we set a proxy to that url. Now if daphne and worker are 
running, we should be able to see our webpage when we visit the url.  