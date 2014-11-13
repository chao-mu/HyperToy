HyperToy
========

A framework for rapidly writing toy http servers and proof of concepts. The idea is that it gives
you full control over low level details while keeping you from having to disable the high level ones. Oh, and it has a built in launcher!

Install
-------

```
$ git clone https://github.com/chao-mu/HyperToy.git
$ cd HyperToy
$ sudo python3 setup.py install 
```

Example - Tarpit
----------------

### Code

```python
#!/usr/bin/env python

import hypertoy

class Tarpit(hypertoy.HyperToyHandler):
  """
  Lead scanners on a wild goose chase generating random links and always responding with a 200.
  """

  def content(self):
    html_template = \
      "<html><head><title>{}</title></head><body><a href='/{}'>{}</a></body></html>\n"

    html = html_template.format(
      hypertoy.random_alphanum(3, 8),
      hypertoy.random_alphanum(3, 8),
      hypertoy.random_alphanum(3, 8)
    )

    return html

if __name__ == "__main__":
  hypertoy.main(Tarpit)
```

### Usage

hypertoy.main instills your handler with magical CLI powers!

#### Server

```
$ python3 examples/tarpit.py  --help
usage: tarpit.py [-h] [--ports PORTS [PORTS ...]] [--host HOST]

Lead scanners on a wild goose chase generating random links and always
responding with a 200.

optional arguments:
  -h, --help            show this help message and exit
  --ports PORTS [PORTS ...]
                        The port to listen on.
  --host HOST           The host to bind to.
$ python3 examples/tarpit.py  --ports 8080 8181 8282
Listening on 127.0.0.1:8080,8181,8282
```

#### Client

```
$ curl -D - localhost:8080
HTTP/1.0 200 OK
Server: Tarpit Fun!
Date: Tue, 07 Oct 2014 20:52:33 GMT
Content-type: text/html
Last-Modified: Tue, 07 Oct 2014 20:52:33 GMT
Content-Length: 82

<html><head><title>fZL</title></head><body><a href='/Kehu'>NLZY</a></body></html>
```
