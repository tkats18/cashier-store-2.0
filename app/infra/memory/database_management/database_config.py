from dataclasses import dataclass
from enum import Enum


class DbType(Enum):
    INMEMORY = ("INMEMORY",)
    SQLLITE = ("SQLLITE",)


@dataclass
class DbConfigurationParams:
    path: str


@dataclass
class DbCreationParams:
    db_type: DbType
    config: DbConfigurationParams
