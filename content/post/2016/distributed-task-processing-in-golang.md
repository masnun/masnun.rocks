+++
author = ""
date = "2016-11-01T22:31:09+06:00"
description = ""
tags = ["Golang"]
title = "Distributed Task Processing in Go"

+++

I started playing with Go almost a year ago but never really managed to dive deeper or do anything serious with 
it. Recently picked it up again, reading and trying out bits of code on and off. Also started this new blog with 
Hugo (which is written in Go as well). As a language, Go is simple yet performant. I am definitely going to 
build a few micro services with Go soon. 

Having said that, I was wondering what I could use to build a distributed task processing system. What I wanted is 
something similar to Celery in the Python land. Luckily, I found 
<a href="https://github.com/RichardKnop/machinery" target="_blank">machinery</a> which is inspired by Celery and 
has nice APIs to achieve similar results. In this blog post, I am going to demonstrate a simple example. 

The source code is available here: <a href="https://github.com/masnun/golang-distributed-task-processing" target="_blank">masnun/golang-distributed-task-processing</a>

### Getting started

Here's what we're going to do:

* There will be at least one worker which will be running and waiting for tasks
* We will be sending task request from another process 
* We will be using Redis as the message queue
* Ideally the setup would be distributed, that is the worker might run in a separate machine. But for this 
example, I will run both the worker and the task sender on the same machine. 

### Get the dependencies

We need to install `machinery` first. I am using Glide for dependency management in this project. But 
that is not compulsory. `go get` should work fine. So first, let's install machinery - 

```sh
go get github.com/RichardKnop/machinery/v1
```

### Writing Task and worker

Workers are processes which keep running, waiting for task requests. Tasks are functions which can be 
requested and then the workers execute those functions and return the results. 

Say we have a task named `Say`. From some other processes, we would request that the `Say` task be executed. 
The worker that will receive the request will find which function is registered as the `Say` task and then
call the function with the received arguments. The result from the function is then stored and can be retrieved 
by the other parties. 

So we first need to write a simple task. We will be writing a function named `Say` which will accept a name and 
say hello. So let's create a directory named `worker` and inside create a file named `hello.go`. In the file, 
let's define this function: 

```go
package main

// Say "Hello World"
func Say(name string) (string, error) {
	return "Hello " + name + "!", nil
}

```

Please note the function signature. The function must return `error` as the second return value. Otherwise
the library will have issues. 

In our case, we will be building a single executable from the worker code. So the package is called main. Now 
that we have a function, let's write the worker. Create a file named `main.go` and put the following contents: 


```go
package main

import (
	machinery "github.com/RichardKnop/machinery/v1"
	"github.com/RichardKnop/machinery/v1/config"
	"github.com/RichardKnop/machinery/v1/errors"
)

func main() {

	var cnf = config.Config{
		Broker:        "redis://127.0.0.1:6379",
		ResultBackend: "redis://127.0.0.1:6379",
	}

	server, err := machinery.NewServer(&cnf)
	if err != nil {
		errors.Fail(err, "Could not create server")
	}

	server.RegisterTask("Say", Say)

	worker := server.NewWorker("worker-1")
	err = worker.Launch()
	if err != nil {
		errors.Fail(err, "Could not launch worker!")
	}

}
```

The code is quite simple. We create a config object by passing the `Broker` and `ResultBackend` values. We are 
using Redis here and the redis server is running on our machine. Please make sure the redis server is up and 
running on that address. Otherwise, change the address to point to a running redis instance. 

Then we construct a server out of the configuration and register the task with the `RegisterTask` method. We 
pass a name and the corresponding function to execute for that task. It becomes simpler if we use the function 
as the task name. Once the task is registered, we need to create one or more worker processes. Here we create a 
new worker instance by calling `NewWorker` method on the server. We pass a worker name so we can identify it 
later on (for example in the logs). We then `Launch` the worker. The worker starts up and connects to our redis 
server. It then subscribes to appropriate channels to start listenning to task requests. 

That's all we need to do to create a task and worker. 

### Requesting / Sending Tasks 

Now from another process (say from a running web application), on a certain ocassion, we want to run a background 
task. Here we will see how we can send task requests. 

In our root directory, let's create another `main.go` file and `main` function to send the tasks. 

```go
package main

import (
	machinery "github.com/RichardKnop/machinery/v1"
	"github.com/RichardKnop/machinery/v1/config"
	"github.com/RichardKnop/machinery/v1/errors"
	"github.com/RichardKnop/machinery/v1/signatures"
)

func main() {

	var cnf = config.Config{
		Broker:        "redis://127.0.0.1:6379",
		ResultBackend: "redis://127.0.0.1:6379",
	}

	server, err := machinery.NewServer(&cnf)
	if err != nil {
		errors.Fail(err, "Can not create server!")
	}

	sayTask := signatures.TaskSignature{
		Name: "Say",
		Args: []signatures.TaskArg{
			signatures.TaskArg{
				Type:  "string",
				Value: "masnun",
			},
		},
	}

	server.SendTask(&sayTask)

}

```

If you look carefully, up to the server creation, the code is same. We define a config and create a server. Then we 
define a task signature. We need to define task signatures to request task executions. In the task signature, 
we need to pass the `Name` of the task and a list of arguments as `Args`. The args will be of `TaskArg` type. Each
`TaskArg` need to set the `Type` and the `Value`. These arguments will be passed along to our function when the worker 
receives this request. 

To queue a task, we use the `SendTask` method and pass a pointer to our `TaskSignature`.


### Tying it out!

Make sure the redis server is running. In case it is not, run it. 

```sh
redis-server
```

Once redis is running, build and run the worker. 

```sh
cd worker
go build
./worker
```

Once the worker starts up, you should see some messages like these: 

```
machinery: worker.go:27: Launching a worker with the following settings:
machinery: worker.go:28: - Broker: redis://127.0.0.1:6379
machinery: worker.go:29: - ResultBackend: redis://127.0.0.1:6379
machinery: worker.go:30: - Exchange:
machinery: worker.go:31: - ExchangeType:
machinery: worker.go:32: - DefaultQueue:
machinery: worker.go:33: - BindingKey:
machinery: redis.go:86: [*] Waiting for messages. To exit press CTRL+C
```

Now we need to build the program that will send tasks to the queue. Open a new terminal window and 
navigate to the project root. Build the main program and run it. 

```
go build -o main
./main
```

That should queue the task. Now switch to the worker process and check the output. If everything goes right, 
we will see some output like: 

```
machinery: redis.go:211: Received new message: {"UUID":"task_c39f7e99-df4d-443a-ad21-3481260b34fb","Name":"Say","RoutingKey":"","GroupUUID":"","GroupTaskCount":0,"Args":[{"Type":"string","Value":"masnun"}],"Headers":null,"Immutable":false,"OnSuccess":null,"OnError":null,"ChordCallback":null}
machinery: worker.go:110: Processed task_c39f7e99-df4d-443a-ad21-3481260b34fb. Result = Hello masnun!
```

Since we are using a `ResultBackend` too, we can check the state and retrieve the task results. 

```go

asyncResult, err := server.SendTask(&sayTask)

taskState := asyncResult.GetState()
fmt.Printf("Current state of %v task is:\n", taskState.TaskUUID)
fmt.Println(taskState.State)

result, err := asyncResult.Get()
fmt.Println(result.Interface())
```

(My example code on Github does not include this part, it would be a good self practice to try these out ourselves,
no?)


The machinery library has some other cool features too. Do checkout the github repo for in depth documentation 
and code samples. 