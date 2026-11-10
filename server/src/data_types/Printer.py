from dataclasses import dataclass
from typing import Optional
import Job

@dataclass(slots=True)
class Printer:
  id:bytes
  name:str
  image:Optional[bytes]
  status:Optional[int]
  ip:Optional[str]
  username:Optional[str]
  key:Optional[str]
  api:Optional[str]
  job:Optional[Job]