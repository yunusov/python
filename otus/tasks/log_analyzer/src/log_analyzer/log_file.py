import datetime
from dataclasses import dataclass


@dataclass
class LogFile:
    path: str | None
    date: datetime.datetime
    ext: str | None
