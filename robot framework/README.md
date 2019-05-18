# robot framework tests

Here a couple of scripts using robot framework. I focused on the CLI use of this automation testing tool. First ipmression is rather bad.

What I like:
+ Cisco support thanks to pyATS library



What I do not like with robot framework:
- I have to learn a new DSL
  * This one is complicated
  * It is hard to see the link between the code and the keywords
- Very few examples using SSH
  * we find the same example on the Internet; the one of SSHLibrary
  * on the Internet most of them are for Web applications
- "CryptographyDeprecationWarning" messages on a correct test because "cryptography" library is not including a fixe requested 5 months ago; that gives the impression of a deprecated piece of software
- 



Installation:

That is the easy part.
```
[root@linux ~]# pip install robotframework
Collecting robotframework
  Downloading https://files.pythonhosted.org/packages/36/c6/6f89c80ac5a526a091bd383ffdfc64c9a68d9df0c775d4b36f03d8e0ac25/robotframework-3.1.1-py2.py3-none-any.whl (601kB)
     |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 604kB 482kB/s
Installing collected packages: robotframework
Successfully installed robotframework-3.1.1
WARNING: You are using pip version 19.1, however version 19.1.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
[root@linux ~]#
```
