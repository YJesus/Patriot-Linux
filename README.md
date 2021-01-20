# Patriot-Linux
Host IDS for desktop users 
Patriot Linux is a  HIDS for desktop users who wants real time graphical alerts when something suspicious happens

Patriot detect:

1- Suspicious process running

![Screenshot](https://github.com/YJesus/Patriot-Linux/blob/main/images/patriot3.png) 

2- New process starting TCP/IP Connection

![Screenshot1](https://github.com/YJesus/Patriot-Linux/blob/main/images/patriot2.png)

3- Auditd alerts

![Screenshot1](https://github.com/YJesus/Patriot-Linux/blob/main/images/patriot1.png)

4- New keyboards plugged

## Installation

You need to configure Auditd with this suggested rules https://github.com/Neo23x0/auditd (you can use your own rules and simply modify keywords in the code)

And then simply download and run python3 patriot.py

Tested in CentOS/Fedora and Debian/Ubuntu
