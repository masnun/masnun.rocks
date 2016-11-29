+++
date = "2016-11-27T07:48:51+06:00"
title = "Django Channels: Using Custom Channels"
description = ""
author = ""
tags = ["Python", "Django"]

+++

In my earlier blog post - [Introduction to Django Channels](http://masnun.rocks/2016/09/25/introduction-to-django-channels/),
I mentioned that we can create our own channels for various purposes. In this blog post, we would discuss where custom channels 
can be useful, what could be the challenges and of course we would see some code examples. But before we begin, please make sure 
you are familiar with the concepts of Django Channels. I would recommend going through the above mentioned post and the official
docs to familiarize yourself with the basics. 

### Our Use Case

Channels is just a queue which has consumers (workers) listenning to it. With that concept in mind, we might be able to think of 
many innovative use cases a queue could have. But in our example, we will keep the idea simple. We are going to use Channels as 
a means of background task processing. 

We will create our own channels for different tasks. There will be consumers waiting for messages on these channels. When we want to 
do something in the background, we would pass it on the appropriate channels & the workers will take care of the tasks. For example,
we want to create a thumbnail of an user uploaded photo? We pass it to the `thumbnails` channel. We want to send a confirmation email, 
we send it to the `welcome_email` channel. Like that. If you are familiar with Celery or Python RQ, this would sound pretty 
familiar to you. 

Now here's my use case - in one of the projects I am working on, we're building APIs for mobile applications. We use BrainTree for 
payment integration. The mobile application sends a `nonce` - it's like a token that we can use to initiate the actual transaction. 
The transaction has two steps - first we initiate it using the nonce and I get back a transaction id. Then I query whether the transaction
succeeded or failed. I felt it would be a good idea to process this in the background. We already have a websocket end point implemented
using Channels. So I thought it would be great to leverage the existing setup instead of introducing something new in the stack. 

### Challenges 

It has so far worked pretty well. But we have to remember that Channels does not gurantee delivery of the messages and there is 
no retrying if a message fails. So we wrote a custom management command that checks the orders for any records that have the nonce
set but no transaction id or there is transaction id but there is no final result stored. We then scheduled this command to run at 
a certain interval and queue up the unfinished/incomplete orders again. In our case, it doesn't hurt if the orders need some 5 to 10 
minutes to process. 

But if we were working on a product where the message delivery was time critical for our business, we probably would have considered 
Celery for the background processing part.  

### Let's see the codes!

First we needed to write a handler. The hadler would receive the messages on the subscribed channel and process them. Here's the handler: 

```python
def braintree_process(message):
    order_data = message.content.get('order')
    order_id = message.content.get('order_id')
    order_instance = Order.objects.get(pk=order_id)

    if order_data:
        nonce = order_data.get("braintree_nonce")
        if nonce:
            # [snipped]

            TRANSACTION_SUCCESS_STATUSES = [
                braintree.Transaction.Status.Authorized,
                braintree.Transaction.Status.Authorizing,
                braintree.Transaction.Status.Settled,
                braintree.Transaction.Status.SettlementConfirmed,
                braintree.Transaction.Status.SettlementPending,
                braintree.Transaction.Status.Settling,
                braintree.Transaction.Status.SubmittedForSettlement
            ]

            result = braintree.Transaction.sale({
                'amount': str(order_data.get('total')),
                'payment_method_nonce': nonce,
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                transaction = braintree.Transaction.find(result.transaction.id)
                if transaction.status in TRANSACTION_SUCCESS_STATUSES:
                    # [snipped]
                else:
                    # [snipped]
            else:
                errors = []
                for x in result.errors.deep_errors:
                    errors.append(str(x.code))

                # [snipped]
```

Then we needed to define a routing so the messages on a certain channel is passed on to this handler. So in our channel routing, we added
this: 

```python
from channels.routing import route
from .channel_handlers import braintree_process

channel_routing = [
    route("braintree_process", braintree_process),
    # [snipped] ...
]

``` 

We now have a routing set and a handler ready to accept messages. So we're ready! All we need to do is to start passing the 
data to this channel. 

When the API receives a `nonce`, it just passes the order details to this channel: 

```python
Channel("braintree_process").send({
    "order": data,
    "order_id": order.id
})
```

And then the workers start working. They accept the message and then starts processing the payment request. 

In our case, we already had the workers running (since they were serving our websocket requests). If you don't have any workers running,
don't forget to run them. 

```
python manage.py runworker
```

If you are wondering about how to deploy channels, I have you covered - [Deploying Django Channels using Daphne](http://masnun.rocks/2016/11/02/deploying-django-channels-using-daphne/)

### Prioritizing / Scaling Channels 

In our project, Django Channels do two things - handling websocket connections for realtime communication, process delayed jobs in 
background. As you can probably guess, the realtime part is more important. In our current setup, the running workers handle both
types of requests as they come. But we want to dedicate more workers to the websocket and perhaps just one worker should keep processing
the payments. 

Luckily, we can limit our workers to certain channels using the `--only-channels` flag. Or alternatively we can exclude certain 
channels by using the `--exclude-channels` flags. 

### Concluding Thoughts

I personally find the design of channels very straightforward, simple and easy to reason about. When Channels get merged into Django, 
it's going to be quite useful, not just for implementing http/2 or websockets, but also as a way to process background tasks with ease
and without introducing third party libraries.  