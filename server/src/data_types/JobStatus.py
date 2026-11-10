from enum import Enum

class JobStatus(Enum):
  COMPLETE = 0
  PRINTING = 1
  PAUSED = 2
  WAITING_CONFIRMATION = 3
  FAILED_GENERIC = 4