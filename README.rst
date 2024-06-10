htping
======

`htping` is a command-line tool that works like `ping`, but instead of sending ICMP packets, it repeatedly makes HTTP GET requests to check if a website is available.

Installation
------------

To install `htping` from PyPI:

```
pip install htping
```

Usage
-----

To use `htping`, simply run it from the command line followed by the URL you want to ping:

```
htping https://www.example.com
```

Options
-------

- `-i`, `--interval`: Interval in seconds between requests (default is 1.0 seconds).

Example
-------

```
htping https://www.example.com -i 2
```

This will send HTTP GET requests to `https://www.example.com` every 2 seconds.

About
-----

`htping` is a simple tool for monitoring the availability and responsiveness of websites by sending periodic HTTP GET requests.