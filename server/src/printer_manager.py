from data_types import Printer, JobStatus
from typing import Optional, Any
import logging

logger = logging.getLogger(f'printer_manager_server.{__name__}')

class PrinterManager:
  def __init__(self):
    self.printers:list[Printer] = []

  def add_printer(self, printer:Printer) -> bool:
    for check in self.printers:
      if check.id == printer.id:
        return False

    self.printers.append(printer)
    return True

  def get_printer(self, id:bytes) -> Optional[Printer]:
    for check in self.printers:
      if check.id == id:
        return check
    return None

  def find_printers(self, status:JobStatus) -> list[Printer]:
    filtered:list[Printer] = []
    for check in self.printers:
      if check.job.status == status.value:
        filtered.append(check)
    return filtered

  def edit_printer(self, id:bytes, settings:dict[str, Any]):
    count:int = 0
    done:bool = False
    for check in self.printers:
      if check.id == id:
        done = True
        count+= 1
        if count > 1:
          logger.error(f'ID {id} exists for more than one printer. Something really bad happened.')
        for key in settings.keys():
          if key != 'id':
            setattr(check, key, settings[key])
          else:
            logger.warning(f'Attempted to change id on an existing printer from {check.id} to {settings[key]} which is not allowed. Ignoring.')
    return done

  def update(self):
    # This is where the program would update data from printers which have an api. Not implemented
    pass