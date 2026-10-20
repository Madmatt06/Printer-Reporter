from enum import Enum

class Request(Enum):
  GET = 0
  ADD = 1
  EDIT = 2

class DataType(Enum):
  CONNECTION_OPERATIONAL = 0
  PRINTER = 1
  JOB = 2

