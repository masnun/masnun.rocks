+++
title = "Deplying Golang Code to AWS Lambda using Apex"
description = ""
author = ""
tags = ["Golang"]
date = "2017-04-04T02:45:30+06:00"

+++

The "Serverless" model is quickly becoming a buzz word in the cloud world. The world "Serverless" used to confuse me, because, hey, if there are no servers, where does my code run? As I found out eventually that there are definitely servers running (and serving) my code in the serverless model. Except, I don't have to manage those servers. I don't have to provision them myself. I just write code and deploy to the cloud. I only pay for the time my code actually runs. I don't have to pay for the idle time. AWS Lambda is such a provider which allows you to deploy "functions" to the cloud that can be triggered on demand - may be via API or some other events from different AWS services. But the problem is AWS Lambda has official support for a limited number of languages - NodeJS, Python, Java and C#. What if I want to use Clojure? Or Rust? Or Golang? 

I happen to be enjoying Golang a lot recently. At work, I have rewritten some of our code in Go and was very impressed by the performance and simplicity of the code. Looks very readable and maintainable. So I was thinking, I would want to write my functions in Go. Luckily, there's [Apex](http://apex.run/). It allows us to easily create AWS Lambda projects and deploy them to the cloud. It even supports a number of officially unsupported language. The project itself was developed in Go and has excellent support for Go itself. In this blog post, I would like to walk through the steps I followed to get started with Golang and Apex. 

## Configure AWS CLI

Apex can read AWS credentials and config and authenticate on behalf of you. These credentials are stored in `~/.aws` under credentials and config files. Instead of writing those files manually, we can simply use the AWS CLI to configure those through a command prompt. 

Install the AWS CLI if you don't have it already:

```
pip install awscli
```

Then run: 

```
aws configure
```

Pass your access key, secret and region. The program would write to appropriate files for you!

Please note, you must have sufficient privileges to use Lambda. Here's the minimal IAM policy that should get you started. 

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "iam:CreateRole",
        "iam:CreatePolicy",
        "iam:AttachRolePolicy",
        "iam:PassRole",
        "lambda:GetFunction",
        "lambda:CreateFunction",
        "lambda:DeleteFunction",
        "lambda:InvokeFunction",
        "lambda:GetFunctionConfiguration",
        "lambda:UpdateFunctionConfiguration",
        "lambda:UpdateFunctionCode",
        "lambda:CreateAlias",
        "lambda:UpdateAlias",
        "lambda:GetAlias",
        "lambda:ListVersionsByFunction",
        "logs:FilterLogEvents",
        "cloudwatch:GetMetricStatistics"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

(The sample is taken from Apex documentation)

## Install Apex

Installation is easy - 

```
curl https://raw.githubusercontent.com/apex/apex/master/install.sh | sh
```

It should download and install the apex cli. 

## Start a New Project

An Apex project is a collection of functions, it can have multiple functions within it. It also contains a `project.json` file for project wide configurations.  To start a project, just run: 

```
apex init
```


The CLI would ask you a few questions - answer them and then the program would generate your project. By default it generates NodeJS sample. Let's say we created a project named `hike`. There will be a `project.json` in the root and a `functions` sub directory. Inside the functions directory, you will find a directory named `hello` containing nodejs file (`index.js`). But we do not want NodeJS, so let's see how we can use Golang.


## Using Golang

Inside your `functions` directory, you will find each function having their own directory. We would create a function named `echo`. Let's create a directory named `echo` and create a file named `main.go` inside the `echo` directory. 

The directory structure should look like: 

```
➜ tree
.
├── functions
│   └── echo
│       └── main.go
└── project.json
```

Here's sample content for the `main.go` file: 

```Golang
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"github.com/apex/go-apex"
)

func main() {
	dev := os.Getenv("APEX_DEV")
	if dev == "DEV" {
		fmt.Println("I am in Dev")
	} else {
		apex.HandleFunc(func(event json.RawMessage, ctx *apex.Context) (interface{}, error) {
			return map[string]string{"hello": "world"}, nil
		})
	}

}

```

Please note: 

* The `github.com/apex/go-apex` library works as the Go runtime for AWS Lambda. It also produces the NodeJS shim which makes it possible to use the officially unsupported languages. This library is a requirement. 

* While it's easy to deploy and run AWS Lambda functions using Apex, there's no way to execute them locally for debugging purposes. But that's no big deal. Our functions should be standalone and individually runnable and testable, they should not be tightly integrated with Apex. 

* For local testing, we set an environment variable. From within the code, we check for that variable to determine whether we're running locally or in production. This is a simple hack but might not be the best way to do it. 

* It is recommended that we use separate accounts/environment for testing. Apex allows to configure multiple environments (testing, staging, production etc) which we can use for isolated testing. 


## Deploy The Code

Deployment is very simple: 

```
apex deploy
```

The above command deploys changes to all functions (including new functions). We can also pass the name of the `function`. Like: 

```
apex deploy echo
```

Once we have deployed the function(s), we can invoke them to see if they're working fine:

```
apex invoke <function name>
```

In our case:

```
➜ apex invoke echo
{"hello":"world"}
```

## Running Locally

Like previously mentioned, it's recommended to maintain separate AWS Accounts / Profiles / Environments for testing / staging / production etc. However, the quick and dirty method is to use an environment variable. 

For locally running the golang code shown before, `cd` into the `echo` directory where our `main.go` file lives. Install any dependencies using `go get` as necessary. Build the code: 

```
go build
```

This should compile the program. You should get a binary file - `echo` in the same directory. You can run it like this: 

```
APEX_DEV=DEV ./echo
```

## Handling Dependencies

Apparently Apex compiles your Go program for Linux and amd64 architecture -- [Source](https://github.com/apex/apex/blob/master/plugins/golang/golang.go#L28) here. So if Go can find the dependenices while compiling, it should be fine. You don't have to do anything extra. 

In my case, anything I `go get` works just fine! However if you want more control on the compilation, you can have a per function, `function.json` file where you can specify build hooks. Check out the [Java](https://github.com/apex/apex/blob/master/_examples/java/functions/with-gradle/function.json#L5) code as an example. 

## Logs & Metrics

These two commands can come very handy while working with Apex: 

```
apex logs <function name>
apex metrics
```

## Where to Go next?

Check out the Apex documentation on their site to know about the different commands and configuration options available. They have excellent documentation. 