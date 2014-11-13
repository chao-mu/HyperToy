#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import hypertoy

# Base class for our SQL Alchemy model
SQLBase = declarative_base()

# Class used to access database.
DBSession = sessionmaker()

def main():
  # Setup the database and SQLALchemy
  engine = sqlalchemy.create_engine("sqlite:///requests.db")
  SQLBase.metadata.create_all(engine)
  DBSession.configure(bind=engine)

  hypertoy.main(RequestLogger)

class RequestLogger(hypertoy.HyperToyHandler): 
  """
  Record HTTP request information in a database. Not for production use.
  """

  def on_request(self):
    db_session = DBSession()

    # Protect us against maliciously long input
    version = self.request_version[:50]
    path = self.path[:3000]
    method  = self.command[:50]

    port = self.options["port"]

    request = HTTPRequest(
      version       = version,
      version_trunc = len(version) != len(self.request_version),
      path          = path,
      path_trunc    = len(path) != len(self.path),
      method        = method,
      method_trunc  = len(method) != len(self.command),
      port          = port
    )

    # Write request to the database
    db_session.add(request)
    db_session.commit()

class HTTPRequest(SQLBase):
  __tablename__ = "http_requests"

  id = Column(Integer, primary_key=True)

  # e.g. HTTP/1.1
  version = Column(String, nullable=False)
  # Indicates whether value was truncated.
  version_trunc = Column(Boolean, nullable=False)

  # e.g. /
  path = Column(String, nullable=False)
  path_trunc = Column(Boolean, nullable=False)

  # The HTTP method for the request, e.g. GET
  method = Column(String, nullable=False)
  method_trunc = Column(Boolean, nullable=False)

  # The port the request went to (as in the server's listening port), e.g. 80
  port = Column(Integer, nullable=False)

if __name__ == "__main__":
  main()
