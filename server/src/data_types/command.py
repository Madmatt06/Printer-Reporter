from enum import Enum

class Request(Enum):
  GET = 0
  ADD = 1
  EDIT = 2

class DataType(Enum):
  CONNECTION_CHECK = 0
  PRINTER = 1
  JOB = 2
