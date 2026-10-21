from enum import Enum

class Request(Enum):
  CONNECTION_CHECK = 0
  GET = 1
  ADD = 2
  EDIT = 3

class DataType(Enum):
  PRINTER = 0
  JOB = 1

