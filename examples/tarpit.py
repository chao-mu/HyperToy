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
