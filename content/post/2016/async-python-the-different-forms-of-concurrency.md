+++
author = ""
date = "2016-10-06T12:10:03+06:00"
description = ""
tags = ["Python"]
title = "Async Python:  The Different Forms of Concurrency"

+++

With the advent of Python 3 the way we're hearing a lot of buzz about "async" and "concurrency", one 
might simply assume that Python recently introduced these concepts/capabilities. But that would be quite
far from the truth. We have had async and concurrent operations for quite some times now. Also many 
beginners may think that `asyncio` is the only/best way to do async/concurrent operations. In this post
we shall explore the different ways we can achieve concurrency and the benefits/drawbacks of them. 

## Defining The Terms

Before we dive into the technical aspects, it is essential to have some basic understanding of the terms 
frequently used in this context. 

#### Sync vs Async 

In Syncrhonous operations, the tasks are executed in sync, one after one. In asynchronous operations, 
tasks may start and complete independent of each other. One async task may start and continue running 
while the execution moves on to a new task. Async tasks don't block (make the execution wait for it's 
completion) operations and usually run in the background. 

For example, you have to call a travel agency to book for your next vacation. And you need to send an 
email to your boss before you go on the tour. In synchronous fashion, you would first call the travel 
agency, if they put you on hold for a moment, you keep waiting and waiting. Once it's done, you start 
writing the email to your boss. Here you complete one task after another. But if you be clever and 
while you are waiting on hold, you could start writing up the email, when they talk to you, you pause 
writing the email, talk to them and then resume the email writing. You could also ask a friend to 
make the call while you finish that email. This is asynchronicity. Tasks don't block one another. 

#### Concurrency and Parallelism 

Concurrency implies that two tasks make progress together. In our previous example, when we 
considered the async example, we were making progress on both the call with the travel agent and 
writing the email. This is concurrency. 

When we talked about taking help from a friend with the call, in that case both tasks would be running 
in parallel. 

Parallelism is in fact a form of concurrency. But parallelism is hardware dependent. For example if 
there's only one core in the CPU, two operations can't really run in parallel. They just share time 
slices from the same core. This is concurrency but not parallelism. But when we have multiple cores, 
we can actually run two or more operations (depending on the number of cores) in parallel.

#### Quick Recap

So this is what we have realized so far: 

<ul>
    <li> <b>Sync:</b> Blocking operations.</li>
    <li> <b>Async:</b> Non blocking operations.</li>
    <li> <b>Concurrency:</b> Making progress together.</li>
    <li> <b>Parallelism:</b> Making progress in parallel.</li>
</ul>

<br/>

<center>
    *Parallelism implies Concurrency. But Concurrency doesn't always mean Parallelism.* 
</center>

<br/>

## Threads & Processes 

Python has had __Threads__ for a very long time. Threads allow us to run our operations concurrently. But there was/is a problem with 
the __Global Interpreter Lock (GIL)__ for which the threading could not provide true parallelism. However, with __multiprocessing__, 
it is now possible to leverage multiple cores with Python. 

#### Threads 

Let's see a quick example. In the following code, the `worker` function will be run on multiple threads, asynchronously and 
concurrently. 

```python 
import threading
import time
import random


def worker(number):
    sleep = random.randrange(1, 10)
    time.sleep(sleep)
    print("I am Worker {}, I slept for {} seconds".format(number, sleep))


for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()

print("All Threads are queued, let's see when they finish!")

```

Here's a sample output from a run on my machine: 

```text
$ python thread_test.py
All Threads are queued, let's see when they finish!
I am Worker 1, I slept for 1 seconds
I am Worker 3, I slept for 4 seconds
I am Worker 4, I slept for 5 seconds
I am Worker 2, I slept for 7 seconds
I am Worker 0, I slept for 9 seconds
```

So you can see we start 5 threads, they make progress together and when we start the threads (and thus executing the worker function), 
the operation does not wait for the threads to complete before moving on to the next print statement. So this is an async operation. 

In our example, we passed a function to the `Thread` constructor. But if we wanted we could also subclass it and implement the code 
as a method (in a more OOP way). 

__Further Reading:__ 

To know about Threads in details, you can follow these resources: 

* https://pymotw.com/3/threading/index.html 

#### Global Interpreter Lock (GIL)

The Global Interpreter Lock aka GIL was introduced to make CPython's memory handling easier and to allow better integrations with C 
(for example the extensions). The GIL is a locking mechanism that the Python interpreter runs only one thread at a time. That is 
only one thread can execute Python byte code at any given time. This GIL makes sure that multiple threads __DO NOT__ run in parallel. 

Quick facts about the GIL: 

* One thread can run at a time. 
* The Python Interpreter switches between threads to allow concurrency.
* The GIL is only applicable to CPython (the defacto implementation). Other implementations like Jython, IronPython don't have GIL. 
* GIL makes single threaded programs fast.
* For I/O bound operations, GIL usually doesn't harm much.
* GIL makes it easy to integrate non thread safe C libraries, thansk to the GIL, we have many high performance extensions/modules written in C.
* For CPU bound tasks, the interpreter checks between `N` ticks and switches threads. So one thread does not block others. 


Many people see the `GIL` as a weakness. I see it as a blessing since it has made libraries like NumPy, SciPy possible which have 
taken Python an unique position in the scientific communities. 

__Further Reading:__ 

These resources can help dive deeper into the GIL: 

* http://www.dabeaz.com/python/UnderstandingGIL.pdf 


#### Processes

To get parallelism, Python introduced the `multiprocessing` module which provides APIs which will feel very similar if you have used 
Threading before. 

In fact, we will just go and change our previous example. Here's the modified version that uses `Process` instead of `Thread`. 

```python

import multiprocessing
import time
import random


def worker(number):
    sleep = random.randrange(1, 10)
    time.sleep(sleep)
    print("I am Worker {}, I slept for {} seconds".format(number, sleep))


for i in range(5):
    t = multiprocessing.Process(target=worker, args=(i,))
    t.start()

print("All Processes are queued, let's see when they finish!")
```

So what's changed? I just imported the `multiprocessing` module instead of `threading`. And then instead of `Thread`, I used 
`Process`. That's it, really! Now instead of multi threading, we are using multiple processes which are running on different core
of your CPU (assuming you have multiple cores). 

With the `Pool` class, we can also distribute one function execution across multiple processes for different input values. If we 
take the example from the official docs: 

```python
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(f, [1, 2, 3]))

```

Here, instead of iterating over the list of values and calling `f` on them one by one, we are actually running the function on 
different processes. One process executes `f(1)`, another runs `f(2)` and another runs `f(3)`. Finally the results are again 
aggregated in a list. This would allow us to break down heavy computations into smaller parts and run them in parallel for faster 
calculation. 


__Further Reading:__ 

* https://pymotw.com/3/multiprocessing/index.html 

#### The `concurrent.futures` module 

The `concurrent.futures` module packs some really great stuff for writing async codes easily. My favorites are the `ThreadPoolExecutor`
and the `ProcessPoolExecutor`. These executors maintain a pool of threads or processes. We submit our tasks to the pool and it 
runs the tasks in available thread/process. A `Future` object is returned which we can use to query and get the result when the task 
has completed. 

Here's an example of `ThreadPoolExecutor`: 

```python
from concurrent.futures import ThreadPoolExecutor
from time import sleep
 
def return_after_5_secs(message):
    sleep(5)
    return message
 
pool = ThreadPoolExecutor(3)
 
future = pool.submit(return_after_5_secs, ("hello"))
print(future.done())
sleep(5)
print(future.done())
print(future.result())
```

I have a blog post on the `concurrent.futures` module here: http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html
which might be helpful for exploring the module deeper. 

__Further Reading:__ 

* https://pymotw.com/3/concurrent.futures/

<br/>

## Asyncio - Why, What and How?

You probably have the question many people in the Python community have - What does asyncio bring new to the table? Why did we need
one more way to do async I/O? Did we not have threads and processes already? Let's see! 

#### Why do we need asyncio?

Processes are costly to spawn. So for I/O, Threads are chosen largely. We know that I/O depends on external stuff - slow disks or 
nasty network lags make I/O often unpredictable. Now, let's assume that we are using threads for I/O bound operations. 3 threads 
are doing different I/O tasks. The interpreter would need to switch between the concurrent threads and give each of them some time 
in turns. Let's call the threads - `T1`, `T2` and `T3`. The three threads have started their I/O operation. `T3` completes it first. 
`T2` and `T1` are still waiting for I/O.  The Python interpreter switches to `T1` but it's still waiting. Fine, so it moves to `T2`, 
it's still waiting and then it moves to `T3` which is ready and executes the code. Do you see the problem here? 

`T3` was ready but the interpreter switched between `T2` and `T1` first - that incurred switching costs  which we could have avoided
 if the interpreter first moved to `T3`, right? 


#### What is asyncio?

 Asyncio provides us an event loop along with other good stuff. The event loop tracks different I/O events and switches to 
 tasks which are  ready and pauses the ones which are waiting on I/O. Thus we don't waste time on tasks which are not ready to run 
 right now. 

 The idea is very simple. There's an event loop. And we have functions that run async, I/O operations. We give our functions to the 
 event loop and ask it to run those for us. The event loop gives us back a `Future` object, it's like a promise that we will get 
 something back in the *future*. We hold on to the promise, time to time check if it has a value (when we feel impatient) and finally
 when the future has a value, we use it in some other operations. 

 Asyncio uses generators and coroutines to pause and resume tasks. You can read these posts for more details: 

* http://masnun.com/2015/11/20/python-asyncio-future-task-and-the-event-loop.html
* http://masnun.com/2015/11/13/python-generators-coroutines-native-coroutines-and-async-await.html


#### How do we use asyncio? 

Before we beging, let's see example codes: 
 
```python
import asyncio
import datetime
import random


async def my_sleep_func():
    await asyncio.sleep(random.randint(0, 5))


async def display_date(num, loop):
    end_time = loop.time() + 50.0
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        if (loop.time() + 1.0) >= end_time:
            break
        await my_sleep_func()


loop = asyncio.get_event_loop()

asyncio.ensure_future(display_date(1, loop))
asyncio.ensure_future(display_date(2, loop))

loop.run_forever()

```

Please note that the `async/await` syntax is Python 3.5+ only. if we walk through the codes: 

* We have an async function `display_date` which takes a number (as an identifier) and the event loop as parameters. 
* The function has an infinite loop that breaks after 50 secs. But during this 50 sec period, it repeatedly prints out the time 
and takes a nap. The `await` function can wait on other async functions (coroutines) to complete. 
* We pass the function to event loop (using the `ensure_future` method). 
* We start running the event loop. 

Whenever the `await` call is made, asyncio understands that the function is probably going to need some time. So it pauses the execution, 
starts monitoring any I/O event related to it and allows tasks to run. When asyncio notices that paused function's I/O is ready, it 
resumes the function. 


## Making the Right Choice

We have walked through the most popular forms of concurrency. But the question remains - when should choose which one? 
It really depends on the use cases. From my experience (and reading), I tend to follow this pseudo code:

```python
if io_bound:
    if io_very_slow:
        print("Use Asyncio")
    else:
       print("Use Threads")
else:
    print("Multi Processing")

``` 

* CPU Bound => Multi Processing
* I/O Bound, Fast I/O => Multi Threading
* I/O Bound, Slow I/O => Asyncio 

