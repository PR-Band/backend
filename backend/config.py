import os
from dataclasses import dataclass


@dataclass
class Config:
    db_url: str


def load():
    return Config(db_url=os.environ['DB_URL'])


config = load()
