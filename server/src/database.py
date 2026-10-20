import logging
import sqlite3, uuid
from pathlib import Path
from typing import Optional
from data_types import Job, Printer

logger = logging.getLogger(f'printer_manager_server.{__name__}')

class Database:
  def __init__(self, database_file:Path):
    self.conn:sqlite3.Connection = sqlite3.connect(database_file)
    self.cursor:sqlite3.Cursor = self.conn.cursor()
    self.cursor.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, name TEXT, start_time INT NOT NULL, end_time INT NOT NULL, image BLOB, status INT NOT NULL, user_id INT, job_id TEXT, public_notify INT, FOREIGN KEY (printer_id) REFERENCES printers_table(id) NOT NULL, CHECK start <= end);')
    self.cursor.execute('CREATE TABLE IF NOT EXISTS printers (id TEXT PRIMARY KEY, name TEXT NOT NULL, image BLOB, status INT, ip TEXT, username TEXT, key TEXT);')

  def add_printer(self, name:str, image:Optional[bytes], status:Optional[int], ip:Optional[str], username:Optional[str], key:Optional[str]):
    printer_id:str = str(uuid.uuid4())
    self.cursor.execute('INSERT INTO printers (id, name, image, status, ip, username, key) VALUES (?, ?, ?, ?, ?, ?, ?);', (printer_id, name, image, status, ip, username, key))
    return printer_id

  def get_printers(self, printing:Optional[bool] = None) -> list[Printer]:
    results = self.cursor.execute('Select * FROM printers;')
    printers: list[Printer] = []
    for row in results.fetchall():
      printers.append(Printer(row[0], row[1], row[2], row[3]))
    return printers

  def add_job(self, name:str, start_time:int, end_time:int, image:Optional[bytes], status:int, user_id:Optional[int], public_notify:int, printer_id:str) -> Optional[str]:
    if end_time < start_time:
      return None
    if status < 0:
      return None
    results = self.cursor.execute('SELECT id FROM jobs WHERE printer_id = ? AND status > 0;', printer_id)
    if results.fetchone() is not None:
      return None
    job_id:str = str(uuid.uuid4())
    try:
      self.cursor.execute('INSERT INTO jobs (id, name, start_time, end_time, image, status, user_id, job_id, printer_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (job_id, name, start_time, end_time, image, status, user_id, public_notify, printer_id))
      self.conn.commit()
    except sqlite3.Error as e:
      logger.error(f'Failed to insert job into table. {e}')
      return None
    return job_id

  def get_current_jobs(self) -> list[Job]:
    results = self.cursor.execute('SELECT * FROM jobs WHERE status IS NULL;')
    jobs:list[Job] = []
    for row in results.fetchall():
      jobs.append(Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    return jobs

  def get_completed_jobs(self) -> list[Job]:
    results = self.cursor.execute('SELECT * FROM jobs WHERE status = 0;')
    jobs: list[Job] = []
    for row in results.fetchall():
      jobs.append(Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    return jobs

  def get_waiting_jobs(self) -> list[Job]:
    results = self.cursor.execute('SELECT * FROM jobs WHERE status = 1;')
    jobs: list[Job] = []
    for row in results.fetchall():
      jobs.append(Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    return jobs

  def get_failed_jobs(self) -> list[Job]:
    results = self.cursor.execute('SELECT * FROM jobs WHERE status > 1;')
    jobs: list[Job] = []
    for row in results.fetchall():
      jobs.append(Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    return jobs

  def get_filtered_jobs(self, status:int) -> list[Job]:
    results = self.cursor.execute('Select * FROM jobs WHERE status = ?;', status)
    jobs: list[Job] = []
    for row in results.fetchall():
      jobs.append(Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    return jobs


