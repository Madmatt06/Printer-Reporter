from dataclasses import dataclass

@dataclass(slots=True)
class Printer:
  id:str
  name:str
  image:bytes
  status:int