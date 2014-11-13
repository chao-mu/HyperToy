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
#!/usr/bin/env python3

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
Server: Apache
Date: Tue, 07 Oct 2014 20:52:33 GMT
Content-type: text/html
Last-Modified: Tue, 07 Oct 2014 20:52:33 GMT
Content-Length: 82

<html><head><title>fZL</title></head><body><a href='/Kehu'>NLZY</a></body></html>
```


Example - Advanced
------------------

### Code

```python

import argparse

import hypertoy

def main():
  app = hypertoy.HyperToyApp(FakeServer)

  app.add_argument("--content_file", nargs='?', type=argparse.FileType('r'))
  app.add_argument("--status", default=555, type=int)
  app.add_argument("--server", default="Funtime Server!")

  args = app.parse_args()

  content = ""
  if args.content_file is not None:
    content = args.content_file.read()

  app.run({"content":content})

class FakeServer(hypertoy.HyperToyHandler): 
  """
  HTTP server defined by command line arguments.
  """

  def content(self):
    return self.options["content"]

  def server_string(self):
    return self.options["server"]

  def status_code(self):
    return self.options["status"]

if __name__ == "__main__":
  main()
```

### Usage

HyperToyApp's run function still gives you a launcher. You will see that
our additional options are now in the help output.

#### Server
```
$ python3 examples/fake_server.py --help                                                                                 
usage: fake_server.py [-h] [--ports PORTS [PORTS ...]] [--host HOST]
                      [--content_file [CONTENT_FILE]] [--status STATUS]
                      [--server SERVER]

HTTP server defined by command line arguments.

optional arguments:
  -h, --help            show this help message and exit
  --ports PORTS [PORTS ...]
                        The port to listen on.
  --host HOST           The host to bind to.
  --content_file [CONTENT_FILE]
  --status STATUS
  --server SERVER
$ python3 examples/fake_server.py --ports 8080 --status 404 --server 'Server wheee!' --content_file content.txt 
```

#### Client

```
$ curl -D - http://localhost:8080/
HTTP/1.0 404 Not Found
Server: Server wheee!
Date: Thu, 13 Nov 2014 16:45:29 GMT
Content-type: text/html
Last-Modified: Thu, 13 Nov 2014 16:45:29 GMT
Content-Length: 5

test
```
