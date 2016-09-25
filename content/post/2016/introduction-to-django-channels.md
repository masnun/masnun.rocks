+++
author = ""
date = "2016-09-25T21:27:34+06:00"
description = ""
tags = ["Python", "Django"]
title = "Introduction to Django Channels"
+++

Django is a brilliant web framework. In fact it is my most favourite one for various reasons. An year and 
a half ago, I switched to Python and Django for all my web development. I am a big fan of the eco system
and the many third party packages. Particularly I use Django REST Framework whenever I need to create 
APIs. Having said that, Django was more than good enough for basic HTTP requests. But the web has changed. 
We now have HTTP/2 and web sockets. Django could not support them well in the past. For the web socket part, 
I usually had to rely on Tornado or NodeJS (with the excellent Socket.IO library). They are good technologies
but most of my web apps being in Django, I really wished there were something that could work with Django itself.
And then we had __Channels__. The project is meant to allow Django to support HTTP/2, websockets or other 
protocols with ease. 


### Concepts ###
The underlying concept is really simple - there are `channels` and there are `messages`, 
there are `producers` and there are `consumers` - the whole system is based on passing messages 
on to channels and consuming/responding to those messages. 

Let's look at the core components of Django Channels first: 

* `channel` - A channel is a FIFO queue like data structure. We can have many channels depending on our need.  
* `message` - A message contains meaningful data for the consumers. Messages are passed on to the channels. 
* `consumer` - A consumer is usually a function that consumes a message and take actions. 
* `interface server` - The interface server knows how to handle different protocols. It works as a translator
or a bridge between Django and the outside world. 

### How does it work? ###

A http request first comes to the `Interface Server` which knows how to deal with a specific type of
request. For example, for websockets and http, __Daphne__ is a popular interface server. When a 
new http/websocket request comes to the interface server (daphne in our case), it accepts the  request 
and transforms it into a `message`.  Then it passes the `message` to the appropriate `channel`. There are 
predefined channels for specific types. For example, all http requests are passed to `http.request` channel. 
For incoming websocket messages, there is `websocket.receive`. So these channels receive the messages when 
the corresponding type of requests come in to the interface server. 

Now that we have `channels` getting filled with `messages`, we need a way to process these messages and 
take actions (if necessary), right? Yes! For that we write some consumer functions and register them to 
the channels we want. When messages come to these channels, the consumers are called with the message. 
They can read the message and act on them. 

So far, we have seen how we can **read** an incoming request. But like all web applications, we should 
**write** something back too, no? How do we do that? As it happens, the interface server is quite clever. 
While transforming the incoming request into a message, it creates a `reply` channel for that particular 
client request and registers itself to that channel. Then it passes the reply channel along with the message.
When our consumer function reads the incoming message, it can pass a response to the `reply channel` attached
with the message. Our interface server is listenning to that reply channel, remember? So when a response is sent
back to the reply channel, the interface server grabs the message, transforms it into a http response and sends 
back to the client. Simple, no?


### Writing a Websocket Echo Server ###

Enough with the theories, let's get our hands dirty and build a simple echo server. The concept is simple. 
The server accepts websocket connections, the client writes something to us, we just echo it back. Plain and 
simple example. 

##### Install Django & Channels #####

```bash
pip install channels
```

That should do the trick and install Django + Channels. Channels has Django as a depdency, so when you install
channels, Django comes with it. 


##### Create An App  #####
Next we create a new django project and app - 

```bash
django-admin.py startproject djchan
```
```bash
cd djchan
```
```bash
python manage.py startapp realtime
```

##### Configure `INSTALLED_APPS` #####
We have our Django app ready. We need to add `channels` and our django app (`realtime`) to the `INSTALLED_APPS` list under `settings.py`. 
Let's do that: 

```python 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "channels",
    "realtime"
]
```

##### Write our Consumer #####

After that, we need to start writing a consumer function that will process the incoming websocket messages 
and send back the response: 

```python
# consumers.py 
def websocket_receive(message):
    text = message.content.get('text')
    if text:
        message.reply_channel.send({"text": "You said: {}".format(text)})

```

The code is simple enough. We receieve a message, get it's text content (we're expecting that the websocket 
connection will send only text data for this exmaple) and then push it back to the `reply_channel` - just like 
we planned. 

##### Channels Routing #####

We have our consume function ready, now we need to tell Django how to route messages to our consumer. Just like 
URL routing, we need to define our channel routings. 

```python
# routing.py
from channels.routing import route
from .consumers import websocket_receive
 
channel_routing = [
    route("websocket.receive", websocket_receive, path=r"^/chat/"),
]
```
The code should be self explanatory. We have a list of `route` objects. Here we select the channel name 
(`websocket.receive` => for receieving websocket messages), pass the consumer function and then configure 
the optional `path`. The path is an interesting bit. If we didn't pass a value for it, the consumer will 
get all the messages in the `websocket.receive` channel on any URL. So if someone created a websocket connection
to `/` or `/private` or `/user/1234` - regardless of the url path, we would get all incoming messages. But 
that's not our intention, right? So we restrict the `path` to `/chat` so only connections made to that url 
are handled by the consumer. Please note the beginning `/`, unlike url routing, in channels, we have to use it. 

##### Configuring The Channel Layers #####

We have defined a consumer and added it to a routing table. We're more or less ready. There's just a final 
bit of configuration we need to do. We need to tell channels two things - which backend we want to use and 
where it can find our channel routing. 

Let's briefly talk about the backend. The messages and the channels - Django needs some sort of data store or 
message queue to back this system. By default Django can use in memory backend which keeps these things in memory
but if you consider a distributed app, for scaling large, you need something else. Redis is a popular and proven 
piece of technology for these kinds of scenarios. In our case we would use the Redis backend. 

So let's install that: 

```sh
pip install asgi_redis
```

And now we put this in our `settings.py`: 

```python 
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

##### Running The Servers #####

Make sure that Redis is running (usually `redis-server` should run it). Now run the django app:

```sh
python manage.py runserver
```

In local environment, when you do `runserver` - Django launches both the interface server and necessary
 background workers (to run the consumer functions in the background). But in production, 
 we should run the workers seperately. We will get to that soon. 

##### Trying it Out! #####

Once our dev server starts up, let’s open up the web app. If you haven’t added any django views, 
no worries, you should still see the “It Worked!” welcome page of Django and that should be 
fine for now. We need to test our websocket and we are smart enough to do that from the dev console. 
Open up your Chrome Devtools (or Firefox | Safari | any other browser’s dev tools) and navigate to the 
JS console. Paste the following JS code:

```javascript

socket = new WebSocket("ws://" + window.location.host + "/chat/");
socket.onmessage = function(e) {
    alert(e.data);
}
socket.onopen = function() {
    socket.send("hello world");
}
```

If everything worked, you should get an alert with the message we sent. Since we defined a path, 
the websocket connection works only on /chat/. Try modifying the JS code and send a message to 
some other url to see how they don’t work. Also remove the path from our route and see how you can catch 
all websocket messages from all the websocket connections regardless of which url they were connected to. 
Cool, no?

##### Our Custom Channels #####

We have seen that certain protocols have predefined channels for various purposes. But we are not limited to those.
We can create our own channels. We don't need to do anything fancy to initialize a new channel. We just need to 
mention a name and send some messages to it. Django will create the channel for us. 

```python 
Channel("thumbnailer").send({
        "image_id": image.id
    })
```

Of course we need corresponding workers to be listenning to those channels. Otherwise nothing will happen. 
Please note that besides working with new protocols, Channels also allow us to create some sort of message 
based task queues. We create channels for certain tasks and our workers listen to those channels. Then we 
pass the data to those channels and the workers process them. So for simpler tasks, this could be a nice
solution. 

### Scaling Production Systems ###

##### Running Workers Seperately #####

On a production environment, we would want to run the workers seperately (since we would not run `runserver` on
production anyway). To run the background workers, we have to run this command: 

```sh
python manage.py runworker
```

##### ASGI & Daphne #####

In our local environment, the `runserver` command took care of launching the Interface server and background 
workers. But now we have to run the interface server ourselves. We mentioned __Daphne__ already. It works 
with the `ASGI` standard (which is commonly used for HTTP/2 and websockets). Just like `wsgi.py`, we now need to 
create a `asgi.py` module and configure it. 

```python
import os
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djchan.settings")

channel_layer = get_channel_layer()
```

Now we can run the server: 

```bash
daphne djchan.asgi:channel_layer
```
If everything goes right, the interface server should start running! 


##### ASGI or WSGI #####

ASGI is still new and WSGI is a battle tested http server. So you might still want to keep using wsgi for your 
http only parts and asgi for the parts where you need channels specific features. 

The popular recommendation is that you should use `nginx` or any other reverse proxies in front and route the 
urls to asgi or uwsgi depending on the url or `Upgrade: WebSocket` header. 

##### Retries and Celery #####

The Channels system does not gurantee delivery. If there are tasks which needs the certainity, it is highly 
recommended to use a system like Celery for these parts. Or we can also roll our own checks and retry logic if
we feel like that. 