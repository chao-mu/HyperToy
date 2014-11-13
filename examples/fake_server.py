#!/usr/bin/env python3

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
