+++
author = ""
date = "2016-10-01T05:27:23+06:00"
description = ""
tags = []
title = "Creating an executable file using Cython"

+++


----
__Disclaimer__: I am quite new to Cython, if you find any part of this post is incorrect or 
there are better ways to do something, I would really appreciate your feedback. Please do feel
free to leave your thoughts in the comments section :)

----
                                    
I know Cython is supposed to be used for building extensions, but I was wondering if we can 
by any chance compile a Python file into executable binary using Cython? I searched on Google and found this 
<a target="_blank" href="http://stackoverflow.com/questions/5105482/compile-main-python-program-using-cython">StackOverflow</a>
question. There is a detailed answer on this question which is very helpful. I tried to follow the 
instructions and after (finding and ) fixing some paths, I managed to do it. I am going to write down
my experience here in case someone else finds it useful as well. 

### Embedding the Python Interpreter 

Cython compiles the Python or the Cython files into C and then compiles the C code to create the 
extensions. Interestingly, Cython has a CLI switch `--embed` whic can generate a `main` function. 
This main function embeds the Python interpreter for us. So we can just compile the C file and 
get our single binary executable. 

### Getting Started

First we need to have a Python (`.py`) or Cython (`.pyx`)  file ready for compilation. Let's start with
a plain old "Hello World" example. 

```python
print("Hello World!")
```

Let's convert this Python file to a C source file with embedded Python interpreter. 

```bash
cython --embed -o hello_world.c hello_world.py
```

It should generate a file named `hello_world.c` in the current directory. We now compile it to an 
executable. 

```bash
gcc -v -Os -I /Users/masnun/.pyenv/versions/3.5.1/include/python3.5m -L /usr/local/Frameworks/Python.framework/Versions/3.5/lib  -o test test.c  -lpython3.5  -lpthread -lm -lutil -ldl
```

Please note you must have the Python source code and dynamic libraries in order to successfully compile 
it. I am on OSX and I use PyEnv. So I passed the appropriate paths and it compiled fine. 

Now I have an executable file, which I can run: 

```bash
$ ./hello_world
Hello World!
```

### Dynamic Linking 

In this case, the executable we produce is dynamically linked to our specified Python version. So this 
may not be fully portable (the libraries will need to be available on target machines). But this should
work fine if we compile against common versions (for example the default version of Python or a version
easily obtainable via the package manager). 

### Including Other Modules

Up untill now, I haven't found any easy ways to include other 3rd party pure python modules (ie. `requests`) 
directly compiled into the binary. However, if I want to split my codes into multiple files,  I can 
create other `.pyx` files and use the `include` statement with those. 

For example, here's `hello.pyx`: 

```cython
cdef struct Person:
    char *name
    int age

cdef say():
    cdef Person masnun = Person(name="masnun", age=20)
    print("Hello {}, you are {} years old!".format(masnun.name.decode('utf8'), masnun.age))

```

And here's my main file - `test.pyx` - 

```cython
include "hello.pyx"

say()
```

Now if I compile `test.pyx` just like above example, it will also include the code in `hello.pyx` and 
I can call the `say` function as if it was in `test.pyx` itself. 

However, shared libraries like PyQt would have no issues - we can compile them as is. So 
basically we can take any PyQt code example and compile it with Cython - it should work fine! 


