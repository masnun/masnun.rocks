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

