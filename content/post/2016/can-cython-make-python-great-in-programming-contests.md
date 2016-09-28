+++
author = ""
date = "2016-09-28T08:00:30+06:00"
description = ""
tags = ["Python", "Cython"]
title = "Can Cython make Python Great in Programming Contests?"

+++

Python is getting very popular as the first programming language in both home and aborad. I know many of the 
Bangladeshi universities have started using Python to introduce beginners to the wonderful world of programming. 
This also seems to be <a target="_blank" href="http://cacm.acm.org/blogs/blog-cacm/176450-python-is-now-the-most-popular-introductory-teaching-language-at-top-u-s-universities/fulltext">the case</a> 
in the US. I have talked to a few friends from other countries and they agree to the fact that 
Python is quickly becoming the language people learn first. A quick <a target="_blank" href="http://bfy.tw/7v1B">google search</a> could explain why Python is 
getting so popular among the learners. 

### Python in Programming Contests  

Recently Python has been been included in ICPC, before that Python has usually had less visibility / presence in programming
contests. And of course there are valid reasons behind that. The defacto implementation of Python - "CPython" is 
quite slow. It's a dynmaic language and that costs in terms of execution speed. C / C++ / Java is way 
faster than Python and programming contests are all about speed / performance. 
Python would allow you to solve problems in less lines of code but you may often hit the time limit. Despite the 
limitation, people have continiously chosen Python to learn programming and solve problems on numerous programming 
related websites. This might have convnced the authority to include Python in ICPC.  But we do not yet know 
which flavor (read implementation) and version of Python will be available to the ICPC contestants. From 
<a target="_blank" href="https://www.quora.com/What-do-you-think-about-the-induction-of-Python-in-ACM-ICPC-2017">different</a> 
<a target="_blank" href="http://codeforces.com/blog/entry/44899">sources</a> I gather that Python will be supported
but the time limit issue remains - it is not guranteed that a problem can be solved within the time limit using 
Python. That makes me wonder, can Cython help in such cases? 

### Introduction to Cython 

From the <a target="_blank" href="http://cython.org/">official website</a>: 

>Cython is an optimising static compiler for both the Python programming language and the extended Cython 
>programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.

With Cython, we can add type hints to our existing Python programs and compile them to make them run faster. 
But what is more awesome is the `Cython` language - it is a superset of Python and allows us to write Python 
like code which performs like C. 

Don't trust my words, see for yourself in the <a target="_blank" href="http://docs.cython.org/en/latest/src/tutorial/cython_tutorial.html">Tutorial</a> 
and <a target="_blank" href="http://docs.cython.org/en/latest/src/userguide/language_basics.html#language-basics"> Cython Language Basics</a>. 


### Cython is Fast 

When I say fast, I really mean - **very very** fast. 

<center>
<img src="/images/cython-vs-c.png" alt="cython vs c" />

 Image Source: <a target="_blank" href="http://ibm.co/20XSZ4F">http://ibm.co/20XSZ4F</a> 
 
 </center>

The above image is taken from an article from IBM Developer Works which shows how Cython compares to C in terms of speed.  

You can also check out these links for random benchmarks from different people: 

* <a target="_blank" href="http://www.matthiaskauer.com/2014/02/a-speed-comparison-of-python-cython-and-c/">Cython beating C++</a>
* <a target="_blank" href="http://prabhuramachandran.blogspot.com/2008/09/python-vs-cython-vs-d-pyd-vs-c-swig.html">Cython being 30% faster than the C++</a>
* <a target="_blank" href="http://aroberge.blogspot.com/2010/01/python-cython-faster-than-c.html">Another Benchmark</a>

And finally, do try yourself and benchmark Cython against C++ and see how it performs! 

Bonus article -- <a href="https://magic.io/blog/uvloop-blazing-fast-python-networking/">Blazing fast Python networking</a> :-) 

### Cython is easy to Setup 

OK, so is it easy to make Cython available in the contest environments? Yes, it is! The **only** requirements of 
Cython is that you must have a **C Compiler** installed on your system along with Python. Any computer used for 
contest programming is supposed to have a C compiler installed anyway. 

We just need one command to install Cython: 

```bash
pip install Cython
``` 

__PS:__ Many Scientific distributions of Python (ie. Anaconda) already ships Cython. 

### Cython in Programming Contests

Since we saw that Cython is super fast and easy to setup, programming contests can make Cython available 
along with CPython to allow the contestants make their programs faster and get along with Java / C++. 
It will make Python an attractive choice for serious problem solving.  

I know the `Cython` language is not exactly Python. It is a superset of the Python language. So beginners might 
not be familiar with the language and that's alright. Beginners can start with Python and start solving the 
easier problems with Python. When they start competitive programming and start hitting the time limits, then 
Cython is one of the options they can choose to make their code run faster. Of course Cython needs some 
understanding of how C works - that's fine too because Cython still feels more productive than writing plain 
old C or C++. 


### Final words

PyPy is already quite popular in the Python community. Dropbox and Microsoft are also working on their Python 
JITs. I believe that someday Python JITs would be as fast as Java / C++.  Today, Python is making programming 
fun for many beginners. I hope with Cython, we can worry less about the time limits and accept Python as a 
fitting tool in our competitive programming contests!