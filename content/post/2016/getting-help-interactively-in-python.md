+++
author = ""
date = "2016-11-01T17:00:51+06:00"
description = ""
tags = ["Python"]
title = "Getting Help Interactively in Python"

+++

Working with a module that you're not familiar with? No internet? Somehow the docs are not accessible? 
Or simply feeling adventourous? Python has you covered. There are a few ways to get 
help Interactively. In this post, we will try a few of them. 

### The `dir` built-in

The `dir` built in is a very helpful one. If you call it without any arguments, that is just
`dir()`, it will return the names available in the current scope. When passed with an argument, 
it would display the available attributes of the passed object (inherited or it's own).  

```python
>>> import os
>>> dir(os)
['CLD_CONTINUED', 'CLD_DUMPED', 'CLD_EXITED', 'CLD_TRAPPED', 'EX_CANTCREAT', 'EX_CONFIG', 'EX_DATAERR', 'EX_IOERR', 'EX_NOHOST', 'EX_NOINPUT', 'EX_NOPERM', 'EX_NOUSER', 'EX_OK', 'EX_OSERR', 'EX_OSFILE', 'EX_PROTOCOL', 'EX_SOFTWARE', 'EX_TEMPFAIL', 'EX_UNAVAILABLE', 'EX_USAGE', 'F_LOCK', 'F_OK', 'F_TEST', 'F_TLOCK', 'F_ULOCK', 'MutableMapping', 'NGROUPS_MAX', 'O_ACCMODE', 'O_APPEND', 'O_ASYNC', 'O_CLOEXEC', 'O_CREAT', 'O_DIRECTORY', 'O_DSYNC', 'O_EXCL', 'O_EXLOCK', 'O_NDELAY', 'O_NOCTTY', 'O_NOFOLLOW', 'O_NONBLOCK', 'O_RDONLY', 'O_RDWR', 'O_SHLOCK', 'O_SYNC', 'O_TRUNC', 'O_WRONLY', 'PRIO_PGRP', 'PRIO_PROCESS', 'PRIO_USER', 'P_ALL', 'P_NOWAIT', 'P_NOWAITO', 'P_PGID', 'P_PID', 'P_WAIT', 'RTLD_GLOBAL', 'RTLD_LAZY', 'RTLD_LOCAL', 'RTLD_NODELETE', 'RTLD_NOLOAD', 'RTLD_NOW', 'R_OK', 'SCHED_FIFO', 'SCHED_OTHER', 'SCHED_RR', 'SEEK_CUR', 'SEEK_END', 'SEEK_SET', 'ST_NOSUID', 'ST_RDONLY', 'TMP_MAX', 'WCONTINUED', 'WCOREDUMP', 'WEXITED', 'WEXITSTATUS', 'WIFCONTINUED', 'WIFEXITED', 'WIFSIGNALED', 'WIFSTOPPED', 'WNOHANG', 'WNOWAIT', 'WSTOPPED', 'WSTOPSIG', 'WTERMSIG', 'WUNTRACED', 'W_OK', 'X_OK', '_Environ', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_execvpe', '_exists', '_exit', '_fwalk', '_get_exports_list', '_putenv', '_spawnvef', '_unsetenv', '_wrap_close', 'abort', 'access', 'altsep', 'chdir', 'chflags', 'chmod', 'chown', 'chroot', 'close', 'closerange', 'confstr', 'confstr_names', 'cpu_count', 'ctermid', 'curdir', 'defpath', 'device_encoding', 'devnull', 'dup', 'dup2', 'environ', 'environb', 'errno', 'error', 'execl', 'execle', 'execlp', 'execlpe', 'execv', 'execve', 'execvp', 'execvpe', 'extsep', 'fchdir', 'fchmod', 'fchown', 'fdopen', 'fork', 'forkpty', 'fpathconf', 'fsdecode', 'fsencode', 'fstat', 'fstatvfs', 'fsync', 'ftruncate', 'fwalk', 'get_blocking', 'get_exec_path', 'get_inheritable', 'get_terminal_size', 'getcwd', 'getcwdb', 'getegid', 'getenv', 'getenvb', 'geteuid', 'getgid', 'getgrouplist', 'getgroups', 'getloadavg', 'getlogin', 'getpgid', 'getpgrp', 'getpid', 'getppid', 'getpriority', 'getsid', 'getuid', 'initgroups', 'isatty', 'kill', 'killpg', 'lchflags', 'lchmod', 'lchown', 'linesep', 'link', 'listdir', 'lockf', 'lseek', 'lstat', 'major', 'makedev', 'makedirs', 'minor', 'mkdir', 'mkfifo', 'mknod', 'name', 'nice', 'open', 'openpty', 'pardir', 'path', 'pathconf', 'pathconf_names', 'pathsep', 'pipe', 'popen', 'pread', 'putenv', 'pwrite', 'read', 'readlink', 'readv', 'remove', 'removedirs', 'rename', 'renames', 'replace', 'rmdir', 'scandir', 'sched_get_priority_max', 'sched_get_priority_min', 'sched_yield', 'sendfile', 'sep', 'set_blocking', 'set_inheritable', 'setegid', 'seteuid', 'setgid', 'setgroups', 'setpgid', 'setpgrp', 'setpriority', 'setregid', 'setreuid', 'setsid', 'setuid', 'spawnl', 'spawnle', 'spawnlp', 'spawnlpe', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe', 'st', 'stat', 'stat_float_times', 'stat_result', 'statvfs', 'statvfs_result', 'strerror', 'supports_bytes_environ', 'supports_dir_fd', 'supports_effective_ids', 'supports_fd', 'supports_follow_symlinks', 'symlink', 'sync', 'sys', 'sysconf', 'sysconf_names', 'system', 'tcgetpgrp', 'tcsetpgrp', 'terminal_size', 'times', 'times_result', 'truncate', 'ttyname', 'umask', 'uname', 'uname_result', 'unlink', 'unsetenv', 'urandom', 'utime', 'wait', 'wait3', 'wait4', 'waitpid', 'walk', 'write', 'writev']
>>>
```

Coupled with `getattr`, you can actually write your own custom utilities to better inspect objects. 

### The `help` built-in

I guess I don't have to tell you how `help`-ful this one can be? 

> Did you know the `help` built in is based on `pydoc.help`?

If you just call `help`  without any arguments, it will launch an interactive help prompt
where you can just type in names and it will display help for that. Here's an example:

```python
>>> help()

Welcome to Python 3.5's help utility!

If this is your first time using Python, you should definitely check out
the tutorial on the Internet at http://docs.python.org/3.5/tutorial/.

Enter the name of any module, keyword, or topic to get help on writing
Python programs and using Python modules.  To quit this help utility and
return to the interpreter, just type "quit".

To get a list of available modules, keywords, symbols, or topics, type
"modules", "keywords", "symbols", or "topics".  Each module also comes
with a one-line summary of what it does; to list the modules whose name
or summary contain a given string such as "spam", type "modules spam".

help> list

help>
```
When you type in `list` and hit enter, it will show you the docs for the `list` built in. To quit, press 
`q`. As described in the text above, typing in "modules", "keywords" etc will list what is available. 

Interestingly the help functionality is built on top of `pydoc` so it will be able to help you with most 
of the installed modules (even the third party ones) as long as the modules have doctstrings available. 
Brilliant, no? 

Now if you call the `help` callable with an argument, it will display help for that item. The above example 
for viewing the docs for `list` can be done this way too: 

```python
>>> help(list)
```

Neat, huh? 

### Using the `pydoc` Module

In the previous section, we mentioned `pydoc`. From the name, you can probably guess what it does. Just to be 
certain, let's try this: 

```python
>>> import pydoc
>>> help(pydoc)
```

As you can read in there, the `pydoc` module generates documentation in html or text format for interactive
usages (like in the previous section). It can read Python source files, parse the docstrings and generate 
helpful information for us. Pydoc module comes with your Python installation. So it is always available to you. 

There are some interesting use cases of this module. You can run it from the command line. Just use 
`pydoc <name>` where the `<name>` is the name of a function, module, class etc. It will display 
the same interactive, generated docs we get from `help(<name>)`. 

And then `pydoc -k <keyword>` would search the keyword in the available modules' synopsis. 

If you would like to browse the docs on a web browser, you can run `pydoc -b` and it will run a 
server and open your browser, pointing to the address of the server. If you would like to set the port 
yourself, use `pydoc -p <port>` and then in the prompt, type "b" to open the browser. You can browse 
the docs and search as needed. 


### The `inspect` Module 

The `inspect` module has some interesting use cases too. It can help us know more about different objects 
in runtime. 

The following functions check for object types:

* `ismodule()`
* `isclass()`
* `ismethod()` 
* `isfunction()` 
* `isgeneratorfunction()` 
* `isgenerator()` 
* `istraceback()` 
* `isframe()` 
* `iscode()` 
* `isbuiltin()`
* `isroutine()`


We can use the `getmembers()` function to get all the members of an object, class or module. We can filter 
the members by passing one of the above functions as the second argument. 

```python
>>> len(inspect.getmembers(os))
284
>>> len(inspect.getmembers(os, inspect.isclass))
9
>>>
```

The `getdoc` function can be used to retrieve available documentation from an object. 

```python
>>> inspect.getdoc(list)
"list() -> new empty list\nlist(iterable) -> new list initialized from iterable's items"
```



