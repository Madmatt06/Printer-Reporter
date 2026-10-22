from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class Job:
  id:bytes
  name:str
  start_time:int
  end_time:int
  image:Optional[bytes]
  status:int
  user_id:Optional[int]
  public_notify:int
  printer_id:str