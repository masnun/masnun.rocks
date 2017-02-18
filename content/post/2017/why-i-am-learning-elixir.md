+++
description = ""
author = ""
tags = ["Elixir"]
title = "Why I am learning Elixir"
date = "2017-02-18T12:12:47+06:00"
+++

Elixir is a new programming language that I have become very fond of. It is a dynamic, functional programming language built on top of the Erlang VM (BEAM). Ever wondered why almost all the telecom companies around the world use Erlang for their telephony systems? There has to be a reason, right? Before we dive into Elixir, it is essential to discuss a bit about Erlang and the VM (BEAM). 

### A brief intro to Erlang 

Erlang was developed by Ericsson and was written in Prolog in it's early days. Erlang proved it's worth as a suitable language that can be used in telephone exchanges but the prolog interpreter was 
too slow for that job. So a group inside Ericsson developed the BEAM VM that compiles Erlang to C. The effort was very successful and in 1998 Ericsson launched their new AXD301 switch - which had  over a million lines of Erlang code. Thanks to the reliability and stability of the new VM, the system managed "nine 9s" uptime. According to [this Wikipedia article](https://en.wikipedia.org/wiki/High_availability#Percentage_calculation), that means less than 31.5569 milliseconds downtime per year. However, Ericsson banned Erlang in it's products because it was "proprietary". This made Armstrong, the creator of the language and other associates leave Ericsson. And the implementation was open sourced at the end of the year. Ericsson eventually lifted that ban and rehired Armstrong back in 2004. 

Telephone exchanges need very stable and reliable systems with massive uptime. Erlang provided that. The Erlang VM also features hot code reloading - so you don't have to restart your software to load new codes. No restart - no downtime. 

Concurrency is another very strong feat of Erlang. In the telcos, it's very important to be able to handle a lot of concurrent operations at a time. Erlang really excels at that - millions of concurrent connections yet no downtime. That's something, no? 

> If somebody came to me and wanted to pay me a lot of money to build a large scale message handling system that really had to be up all the time, could never afford to go down for years at a time, I would unhesitatingly choose Erlang to build it in.\
> <br/>
> -- Tim Bray, Director of Web Technologies, Sun Microsystems in OSCON, July 2008 

Erlang comes with the OTP framework which includes some ready to use components and design patterns to follow for building robust Erlang applications. Erlang is often called "Erlang/OTP" because of this accompanying framework. 

We have seen the battle proven track record of Erlang in Telcos. But that's not all. Erlang has been adopted in modern day applications too. For example WhatsApp used Erlang to build and scale their messaging platform across millions of their users. Facebook also used Erlang for their chat infrastructure. 

> If Java is 'write once, run anywhere', then Erlang is 'write once, run forever'.
> <br/><br/>
> -- Joe Armstrong, Creator of Erlang, 2013

### Why do we need Elixir? 

So Erlang is successful and battle tested, matured over the last 25 years or so, then why do we need a new language? Well, Erlang itself is very robust, scalable, matured but the syntax of the language was not easily approachable for me. And I believe in that context, I am not alone. 

On the other hand, Elixir as a language is relatively much easier to start and grasp. I, for example, have never really felt motivated enough to learn Erlang. But Elixir has been  a totally different experience. I did some reading. Liked the syntax, kept on reading, got hooked. Read a book and now I am writing a blog post praising the language. So I would say Elixir is much more approachable than Erlang with the same benefits. 

Elixir uses the same BEAM VM and offers the same advantages of Erlang - fault tolerance, scalability, easy concurrency while being a very productive language for the beginners (and of course for the more advanced users). Performance + Productivity = Win. 

The interoperability between Erlang and Elixir is also excellent. We can use Erlang standard library as well as third party packages from inside Elixir. So despite being a new language, Elixir can already leverage the underlying maturity of the VM and the years of hard work done in the Erlang eco system. 

### Why I am so excited about Elixir? 

In my day to day work, I am mostly a web developer. I have done my share of PHP and then moved on to Python. Today, I am a Python developer with most of my work being in Django. I absolutely love Django as the framework. But then I noticed Phoenix and Elixir. Some of the blog posts I came across heavily motivated me to explore both Elixir and Phoenix. 

* [Elixir / Phoenix is awesome at handling websocket / real time communication](https://hashrocket.com/blog/posts/websocket-shootout)

* [Just look at the availability, scalability and response time - Phoenix Channels vs Rails Action Cable](https://dockyard.com/blog/2016/08/09/phoenix-channels-vs-rails-action-cable)

* [Phoenix is very fast, very performant](https://github.com/mroth/phoenix-showdown)  

* [Many people are using it in production](https://github.com/doomspork/elixir-companies)

* [Pinterest](https://medium.com/@Pinterest_Engineering/introducing-new-open-source-tools-for-the-elixir-community-2f7bb0bb7d8c#.on9d0vf5m)

* [Bleacher Report handles 8x more traffic](http://www.techworld.com/apps/how-elixir-helped-bleacher-report-handle-8x-more-traffic-3653957/)


Not to mention I have played around a bit with a new Phoenix app. It was very easy to get started and everything made sense. I tried making some changes to see how it can fit my requirements. Surprisingly, achieving what I wanted to do didn't take me much time although I was just a beginner. These things really attracted me. The community is very friendly and helpful. The tooling was superb (in fact much much better than what I am generally used to).

With the growth of IoT, we will gradually feel the need of languages and platforms which can handle more and more concurrent connections. Elixir with Erlang and OTP in it's back, will become one of the major players in the IoT arena. 

In short - I felt that Phoenix really delivers on it's promise. It's very performant while I am being productive. I am pretty hopeful that Elixir and Phoenix will be a very good choice for what I do at work. 


### Where to learn about Elixir? 

I really liked the wonderful Elixir School. The official documentation is also excellent. If you want to know what's happening in the community, do keep an eye on Twitter, follow some key people. The Elixir subreddit is also a good place. And of course, don't forget to join the Elixir Slack. 

* [Elixir School](https://elixirschool.com/)
* [Official Guides](https://elixir-slackin.herokuapp.com/)
* [Docs](http://elixir-lang.org/docs.html)
* [Elixir Slack](https://elixir-slackin.herokuapp.com/)
* [Awesome Elixir](https://github.com/h4cc/awesome-elixir)
* [Elixir Fountain](http://elixirfountain.com/)
* [Elixir Casts](https://elixircasts.io/)
* [Elixir Subreddit](https://www.reddit.com/r/elixir/)
* [Elixir Status](https://elixirstatus.com/) 
* [Elixir Weekly](https://elixirweekly.net/)

If you're looking for book recommendation or other resources, checkout the [Learning](http://elixir-lang.org/learning.html) section on the official Elixir website. 

### Does Elixir look difficult/hard? 

Thought I must warn you - since Elixir is a functional programming language, it might take some time to get used to some parts of it, specially for those of us who have been playing in the object oriented world for too long. If you find parts of the language not so comfortable, skip that for the time being and explore other niceties. Some of the functional concepts might take a little time to comprehend but that's alright. Give it some time and once you grasp the concepts, it will blow your mind away. You would love the power, flexibility and the expressiveness very soon. 

