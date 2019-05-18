# robot framework tests

Here a couple of scripts using robot framework. I focused on the CLI use and the network device automation use of this automation testing tool. The first impression is rather bad.

** What I like**:
+ It is possible to the command on a Linux system and testing the answer
+ Cisco support thanks to pyATS library... but there are very little documentation on the official site and no way to send a command clearly explained
+ RENAT is a tool for Robot framework that suport Cisco and IOS devices. But impossible to install (see below).




What I do not like with robot framework:
- I have to learn a new DSL (again another one...)
  * This one is complicated
  * It is hard to see the link between the code and the keywords
- Very few examples using SSH
  * we find the same example on the Internet; the one of SSHLibrary
  * on the Internet most of them are for Web applications
- "CryptographyDeprecationWarning" messages on a correct test because "cryptography" library is not including a fixe requested 5 months ago; that gives the impression of a deprecated piece of software
- RENAT library has issues:
  * RENAT installation is unclear, no pip install and "docker pull bachng/renat:latest" gives the following error message: "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?" even though docker deamon is running
  * RENAT is designed for Python 2.7
  * RENAT "simple scenario" according to the online documentation:
![image](https://bachng2017.github.io/RENAT/doc/renat_sample.png)
  Easy? Clearly not.


** Installation **:

That is the only easy part. Root rights needed.
```
[root@linux ~]# pip install robotframework
Collecting robotframework
  Downloading https://files.pythonhosted.org/packages/36/c6/6f89c80ac5a526a091bd383ffdfc64c9a68d9df0c775d4b36f03d8e0ac25/robotframework-3.1.1-py2.py3-none-any.whl (601kB)
     |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 604kB 482kB/s
Installing collected packages: robotframework
Successfully installed robotframework-3.1.1
[root@linux ~]#
```

Below the usual Linux CLI test. This test is sending an echo to a linux host then check if the result of the echo command is correct.


```
*** Settings ***
Library                SSHLibrary
Suite Setup            Open Connection And Log In
Suite Teardown         Close All Connections

*** Variables ***
${HOST}                10.0.2.15
${USERNAME}            root
${PASSWORD}            root

*** Keywords ***
Open Connection And Log In
   Open Connection     ${HOST}
   Login               ${USERNAME}        ${PASSWORD}

*** Test Cases ***
Execute Command And Verify Output
    ${output}=         Execute Command    echo Hello world!
    Should Be Equal    ${output}          Hello world!

```

And the result:

```
[user@linux tests]$ robot ssh_test.robot
==============================================================================
Ssh Test :: This example demonstrates executing a command on a remote machine
==============================================================================
/home/linux/prog/venv/project1/lib/python3.7/site-packages/paramiko/kex_ecdh_nist.py:39: CryptographyDeprecationWarning: encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.
  m.add_string(self.Q_C.public_numbers().encode_point())
/home/linux/prog/venv/project1/lib/python3.7/site-packages/paramiko/kex_ecdh_nist.py:96: CryptographyDeprecationWarning: Support for unsafe construction of public numbers from encoded data will be removed in a future version. Please use EllipticCurvePublicKey.from_encoded_point
  self.curve, Q_S_bytes
/home/linux/prog/venv/project1/lib/python3.7/site-packages/paramiko/kex_ecdh_nist.py:111: CryptographyDeprecationWarning: encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.
  hm.add_string(self.Q_C.public_numbers().encode_point())
Execute Command And Verify Output :: Execute Command can be used t... | PASS |
------------------------------------------------------------------------------
Ssh Test :: This example demonstrates executing a command on a rem... | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
==============================================================================
Output:  /home/linux/prog/venv/project1/robot/tests/output.xml
Log:     /home/linux/prog/venv/project1/robot/tests/log.html
Report:  /home/linux/prog/venv/project1/robot/tests/report.html
[user@linux tests]$
```




