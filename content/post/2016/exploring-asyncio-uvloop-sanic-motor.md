+++
title = "Exploring Asyncio - uvloop, sanic and motor"
description = ""
author = ""
tags = ["Python"]
date = "2016-11-17T03:33:38+06:00"

+++

The `asyncio` package was introduced in the standard library from Python 3.4. The package is still in provisional stage, that is 
backward compatibility can be broken with future changes. However, the Python community is pretty excited about it and I know 
personally that many people have started using it in production. So, I too decided to try it out. I built a rather simple 
micro service using the excellent `sanic` framework and `motor` (for accessing mongodb). `uvloop` is an alternative event loop
implementation written in Cython on top of libuv and can be used as a drop in replacement for asyncio's event loop. Sanic uses 
`uvloop` behind the scene to go fast. 

In this blog post, I would quickly introduce the technologies involved and then walk through some sample code with relevant explanations.



### What is Asyncio? Why Should I Care? 

In one of my earlier blog post - [Async Python: The Different Forms of Concurrency](http://masnun.rocks/2016/10/06/async-python-the-different-forms-of-concurrency/),
I have tried to elaborate on the different ways to achieve concurrency in the Python land. In the last part of the post, I have tried 
to explain what asyncio brings new to the table. 

Asyncio allows us to write asynchronous, concurrent programs running on a single thread, using an event loop to schedule tasks and 
multiplexing I/O over sockets (and other resources). The one line explanation might be a little complex to comprehend at a glance. So 
I will break it down. In asyncio, everything runs on a single thread. We use coroutines which can be treated as small units of task 
that we can pause and resume. Then there is I/O multiplexing - when our tasks are busy waiting for I/O, an event loop pauses them 
and allows other tasks to run. When the paused tasks finish I/O, the event loop resumes them. This way even a single thread can 
handle / serve a large number of connections / clients by effectively juggling between "active" tasks and tasks that are waiting 
for some sort of I/O. 

In general synchronous style, for example, when we're using thread based concurrency, each client will occupy a thread and when 
we have a large number of connections, we will soon run out of threads. Though not all of those threads were active at a given time, 
some might have been simply waiting for I/O, doing nothing. Asyncio helps us solve this problem and provides an efficient solution 
to the concurrency problem. 

While Twisted, Tornado and many other solutions have existed in the past, NodeJS brought huge attention to this kind of solution. 
And with Asyncio being in the standard library, I believe it will become the standard way of doing async I/O in the Python world over 
time.  

### What about uvloop? 

We talked about event loop above. It schedules the tasks and deals with various events. It also manages the I/O multiplexing using 
the various options offered by the operating system. In simple words - the event loop is very critical and the central part of the 
whole asyncio operations. The `asyncio` package ships with an event loop by default. But we can also swap it for our custom 
implementations if we need/prefer. `uvloop` is one such event loop that is very very fast. The key to it's success could be partially
attributed to Cython. Cython allows us to write codes in Python like syntax while the codes perform like C. `uvloop` was written in 
Cython and it uses the famous `libuv` library (also used by NodeJS). 

If you are wondering if `uvloop`'s performances are good enough reason to swap out the default event loop, you may want to read this 
aricle here - [uvloop: Blazing fast Python networking](https://magic.io/blog/uvloop-blazing-fast-python-networking/) or you can just
look at this following chart taken from that blog post: 

<img src="http://i.imgur.com/0iMUePy.png" />


Yes, it can go faster than NodeJS and catch up to Golang. Convinced yet? Let's talk about Sanic! 

### Sanic - Gotta go fast! 

Sanic was inspired by the above article I talked about. They used `uvloop` and `httptools` too (referenced in the article). The 
framework provides a nice, Flask like syntax along with the `async / await` syntax from Python 3.5.

<strong>Please Note:</strong> `uvloop` still doesn't work on Windows properly. Sanic uses the default asyncio event loop if uvloop 
is not available. But this probably doesn't matter because in most cases we deploy to linux machines anyway. Just in case you 
want to try out the performance gains on Windows, I recommend you use a VM to test it inside a Linux machine. 

### Motor 

Motor started off as an async mongodb driver for Tornado. Motor = <strong>Mo</strong>ngodb + <strong>Tor</strong>nado. But Motor 
now has pretty nice support for asyncio. And of course we can use the `async / await` syntax too. 

I guess we have had brief introductions to the technologies we are going to use. So let's get started with the actual work. 

### Setting Up

We need to install `sanic` and `motor` using `pip`. 

```
pip install sanic
pip install motor
```

Sanic should also install it's dependencies including `uvloop` and `ujson` along with others. 

### Set `uvloop` as the event loop 

We will swap out the default event loop and use `uvloop` instead. 

```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```

Simple as that. We import asyncio and uvloop. We set the event loop policy to uvloop's event loop policy and we're done. Now 
asyncio will use uvloop as the default event loop. 

### Connecting to Mongodb

We will be using `motor` to connect to our mongodb. Just like this: 

```python
from motor.motor_asyncio import AsyncIOMotorClient

mongo_connection = AsyncIOMotorClient("<mongodb connection string>")

contacts = mongo_connection.mydatabase.contacts
```

We import the `AsyncIOMotorClient` and pass our mongodb connection string to it. We also point to our target collection
using a name / variable so that we can easily (and directly) use that collection later. Here `mydatabase` is the db name 
and `contacts` is the collection name. 

### Request Handlers 

Now we will dive right in and write our request handlers. For our demo application, I will create two routes. One for listing 
the contacts and one for creating new ones. But first we must instantiate sanic. 

```python
from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)
```

Flask-like, remember? Now that we have the `app` instance, let's add routes to it. 

```python
@app.route("/")
async def list(request):
    data = await contacts.find().to_list(20)
    for x in data:
        x['id'] = str(x['_id'])
        del x['_id']

    return json(data)


@app.route("/new")
async def new(request):
    contact = request.json
    insert = await contacts.insert_one(contact)
    return json({"inserted_id": str(insert.inserted_id)})

```

The routes are simple and for the sake of brevity, I haven't written any error handling codes. The `list` function is `async`. 
Inside it we `await` our contacts to arrive from the database, as a list of 20 entries. In a sync style, we would use the `find` 
method directly but now we `await` it. 

After we have the results, we quickly iterate over the documents and add `id` key and remove the `_id` key. The `_id` key is an 
instance of `ObjectId` which would need us to use the `bson` package for serialization. To avoid complexity here, we just convert 
the id to string and then delete the ObjectId instance. The rest of the document is usual string based key-value pairs (`dict`).
So it should serialize fine.  

In the `new` function, we grab the incoming json payload and pass it to the `insert_one` method directly. `request.json` would 
contain the `dict` representation of the json request. Check out [this page](https://github.com/channelcat/sanic/blob/master/docs/request_data.md)
for other request data available to you. Here, we again `await` the `insert_one` call. When the response is available, we 
take the `inserted_id` and send a response back. 

### Running the App

Let's see the code first: 

```python
loop = asyncio.get_event_loop()

app.run(host="0.0.0.0", port=8000, workers=3, debug=True, loop=loop)
```

Here we get the default event loop and pass it to `app.run` along with other obvious options. With the `workers` argument, 
we can set how many workers we want to use. This allows us to spin up multiple workers and take advantages of multiple cpu 
cores. On a single core machine, we can just set it to 1 or totally skip that one. 

The `loop` is optional as well. If we do not pass the loop, sanic will create a new one and set it as the default loop. But in 
our case, we have connected to mongodb using motor before the `app.run` function could actually run. Motor now already uses the 
default event loop. If we don't pass that same loop to sanic, sanic will initialize a new event loop. Our database access and 
sanic server will be on two different event loops and we won't be able to make database calls. That is why we use the `get_event_loop`
function to retrieve the current default event loop and pass it to sanic. This is also why we set `uvloop` as the default event 
loop on top of the file. Otherwise we would end up with the default loop (that comes with asyncio) and sanic would also have to 
use that. Initializing `uvloop` at the beginning makes sure everyone uses it. 


### Final Code 

So here's the final code. We probably should clean up the imports and bring them up on top. But to relate to the different steps, 
I kept them as is. Also as mentioned earlier, the code has no error handling. We should write proper error handling code in all 
serious projects. 


```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())



from motor.motor_asyncio import AsyncIOMotorClient

mongo_connection = AsyncIOMotorClient("<connection string>")

contacts = mongo_connection.mydatabase.contacts


from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.route("/")
async def list(request):
    data = await contacts.find().to_list(20)
    for x in data:
        x['id'] = str(x['_id'])
        del x['_id']

    return json(data)


@app.route("/new")
async def new(request):
    contact = request.json
    insert = await contacts.insert_one(contact)
    return json({"inserted_id": str(insert.inserted_id)})


loop = asyncio.get_event_loop()

app.run(host="0.0.0.0", port=8000, workers=3, debug=True, loop=loop)

```

Now let's try it out? 

### Trying Out 

I have saved the above code as `main.py`. So let's run it. 

```sh
python main.py
```

Now we can use `curl` to try it out. Let's first add a contact: 

```sh
curl -X POST -H "Content-Type: application/json" -d '{"name": "masnun"}' "http://localhost:8000/new"

```
We should see something like: 

```
{"inserted_id":"582ceb772c608731477f5384"}
```

Let's verify by checking `/` - 

```
curl -X GET "http://localhost:8000/"
```

If everything goes right, we should see something like:

```
[{"id":"582ceb772c608731477f5384","name":"masnun"}]
```

I hope it works for you too! :-)

If you have any feedback or suggestions, please feel free to share it in the comments section. I would love to disqus :-) 