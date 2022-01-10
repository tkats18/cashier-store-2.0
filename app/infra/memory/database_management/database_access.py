from pathlib import Path
from sqlite3 import Connection
from typing import Any, Protocol


class IDatabaseAccessObject(Protocol):
    def get_access_object(self) -> Any:
        pass


class InMemoryDatabaseAccessObject(IDatabaseAccessObject):
    def __init__(self, db_directory_path: Path):
        self.db_directory_path = db_directory_path

    def get_access_object(self) -> Any:
        return self.db_directory_path


class SqlLiteDatabaseAccessObject(IDatabaseAccessObject):
    def __init__(self, db_connection: Connection):
        self.db_connection = db_connection

    def get_access_object(self) -> Any:
        return self.db_connection
