import argparse
import http.server
import inspect
import random
import string
import threading

def main(handler):
  app = HyperToyApp(handler)

  pretty_ports = ','.join(map(str, app.ports))
  print("Listening on {}:{}".format(app.host, pretty_ports))

  app.run()

class HyperToyApp(object):

  def __init__(self, handler, description=None):
    """
    handler - The class of the HyperToyHandler implementation.
    description - Description for --help. Defaults to class docstring.
    """

    self.handler = handler

    if description is None:
      description = inspect.getdoc(handler)

    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument(
      "--ports",
      default = [8080],
      nargs   = "+",
      type    = int,
      help    = "The port to listen on."
    )
    arg_parser.add_argument(
      "--host",
      default = "127.0.0.1",
      help = "The host to bind to."
    )
    self._arg_parser = arg_parser

  def parse_args(self):
    """
    Returns a Namespace of argument values.
    """
    return self._arg_parser.parse_args()

  @property
  def args(self):
    return self.parse_args()

  def add_argument(self, *args, **kwargs):
    """
    See documentation for ArgumentParser.add_argument.
    """
    self._arg_parser.add_argument(*args, **kwargs)

  @property
  def host(self):
    return self.args.host

  @property
  def ports(self):
    return self.args.ports

  def run(self, handler_options={}):
    # Copy command line arguments to handler options.
    for key, value in vars(self.args).items():
      if key not in handler_options:
        handler_options[key] = value

    server = HyperToyServer(self.handler, self.host, self.ports, handler_options)
    server.run()

class HyperToyServer(object):

  def __init__(self, handler, host, ports, handler_options={}):
    """
    handler - Class of HyperToyHandler implementation.
    host - Host address to bind to.
    ports - Array of ports to listen on.
    handler_options - Dict to provide handlers via attribute "options".
    """
    self.reference_handler = handler
    self.handler_options = handler_options
    self.ports = ports
    self.host = host

  def make_handlers(self):
    handlers = []
    for port in self.ports:
      inner_options = self.handler_options.copy()
      inner_options["port"] = port

      class handler(self.reference_handler):
        options = inner_options

      handlers.append(handler)

    return handlers
    
  def make_servers(self):
    servers = []
    for handler in self.make_handlers():
      host = self.host
      port = handler.options["port"]
      servers.append(http.server.HTTPServer((host, port), handler))

    return servers

  def run(self):
    threads = []

    for server in self.make_servers():
      thread = threading.Thread(target=server.serve_forever)
      thread.start()
      threads.append(thread)

    while True in [thread.is_alive() for thread in threads]:
      pass

class HyperToyHandler(http.server.BaseHTTPRequestHandler):

  def server_headers(self, content):
    """
    HTTP response headers as an array of tuples.
    Default contains Content-type, Last-Modified, and Content-Length. 
    """
    return [
      ("Content-type", "text/html"),
      ("Last-Modified", self.date_time_string()),
      ("Content-Length", str(len(content)))
    ]

  def content(self):
    """
    The body of the HTTP response. Default is an empty string.
    """
    return ""

  def status_code(self):
    """
    The HTTP status code sent in the response. Default is 200.
    """
    return 200

  def server_string(self):
    """
    The server string header. Override to provide one other than the default
    of "Apache".
    """
    return "Apache"

  def version_string(self):
    return self.server_string()

  def on_request(self):
    """
    Called right before response is generated.
    """

  def on_response(self, content, headers, code):
    """
    Called right after response is generated, but before it is sent.
    """

  def send_all(self, content=None, headers=None, code=None):
    # Note, on_request() was put here and not handle/handle_one_request because they handle
    # parsing and other logic we want to happen first (e.g. parsing the request).
    # log_request is also a no-go as it is called by send_response, which comes
    # after we generate our content.
    self.on_request()

    if content is None:
      content = self.content()

    if headers is None:
      headers = self.server_headers(content)

    if code is None:
      code = self.status_code()

    self.on_response(content, headers, code)

    # Send status code
    self.send_response(code)

    # Send headers
    for header in headers:
      self.send_header(header[0], header[1])
    self.end_headers()

    # Send content
    self.wfile.write(content.encode())
 
  def send_error(self, code, message=None):
    """
    Instead of sending an error response as this method should,
    we hijack the error reporting attempt and wrap send_all.
    
    In the case a loop is detected, we call the parent's implementation of send_error.
    """
    # If there was not a corresponding do_ handler (e.g. do_GET), trigger our logic.
    if code == 501:
      self.send_all()
    else:
      super().send_error(code, message) 

def random_alphanum(min_length, max_length):
  """
  Generate a string of ascii letters and digits, between min_length and
  max_length, inclusive.
  """
  return random_string(string.ascii_letters + string.digits, min_length, max_length)

def random_string(charset, min_length, max_length):
  """
  Generate a string from the given character set (charset), between min_length
  and max_length, inclusive.
  """
  length = random.randint(min_length, max_length)

  return ''.join([random.choice(charset) for i in range(length)])
