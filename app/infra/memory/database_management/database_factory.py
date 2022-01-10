import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from app.infra.memory.database_management.database_access import (
    IDatabaseAccessObject,
    InMemoryDatabaseAccessObject,
    SqlLiteDatabaseAccessObject,
)
from app.infra.memory.database_management.database_config import (
    DbConfigurationParams,
    DbCreationParams,
    DbType,
)
from app.infra.memory.entity_management.entity_builder import Entity
from app.infra.memory.entity_management.entity_init_startegy import IEntityInitializer
from app.infra.memory.in_memory.in_memory_product_repository import ProductInMemory
from app.infra.memory.in_memory.in_memory_receipt_c_repository import (
    ReceiptComponentInMemory,
)
from app.infra.memory.in_memory.in_memory_receipt_repository import ReceiptInMemory
from app.infra.memory.sql_lite.sql_lite_product_repository import (
    ProductSqlLite,
)
from app.infra.memory.sql_lite.sql_lite_receipt_c_repository import (
    ReceiptComponentSqlLite,
)
from app.infra.memory.sql_lite.sql_lite_receipt_repository import (
    ReceiptSqlLite,
)
from app.infra.memory.storage_interface.product_protocol import IProductDb
from app.infra.memory.storage_interface.receipt_component_protocol import (
    IReceiptComponentDb,
)
from app.infra.memory.storage_interface.receipt_protocol import IReceiptDb


class IDatabaseFactory(Protocol):
    params: DbConfigurationParams

    def create_database(self) -> IDatabaseAccessObject:
        pass


@dataclass
class InMemoryDatabaseFactory:
    params: DbConfigurationParams

    def create_database(self) -> InMemoryDatabaseAccessObject:
        os.mkdir(self.params.path.join("data"))
        return InMemoryDatabaseAccessObject(Path(self.params.path.join("data")))


@dataclass
class SqlLiteDatabaseFactory:
    params: DbConfigurationParams

    def create_database(self) -> SqlLiteDatabaseAccessObject:
        datasource = sqlite3.connect(self.params.path, check_same_thread=False)
        return SqlLiteDatabaseAccessObject(datasource)


# --------------------------------------------


class DatabaseConfiguration:
    def __init__(self, params: DbCreationParams):
        self.params = params
        if self.params.db_type == DbType.SQLLITE:
            self.db_access: IDatabaseAccessObject = SqlLiteDatabaseFactory(
                params=self.params.config
            ).create_database()
        elif self.params.db_type == DbType.INMEMORY:
            self.db_access = InMemoryDatabaseFactory(
                params=self.params.config
            ).create_database()
        else:
            raise RuntimeError(f"invalid database type {self.params.db_type.name}")

    def product_repository(
        self, entity: Entity, initializer: IEntityInitializer, drop_if_exists: bool
    ) -> IProductDb:

        if self.params.db_type == DbType.SQLLITE:
            repo = ProductSqlLite(entity, self.db_access, drop_if_exists)
        else:
            repo = ProductInMemory(entity, self.db_access, drop_if_exists)

        initializer.init(repo)
        return repo

    def receipt_repository(
        self, entity: Entity, initializer: IEntityInitializer, drop_if_exists: bool
    ) -> IReceiptDb:
        if self.params.db_type == DbType.SQLLITE:
            repo = ReceiptSqlLite(entity, self.db_access, drop_if_exists)
        else:
            repo = ReceiptInMemory(entity, self.db_access, drop_if_exists)

        initializer.init(repo)
        return repo

    def receipt_component_repository(
        self, entity: Entity, initializer: IEntityInitializer, drop_if_exists: bool
    ) -> IReceiptComponentDb:
        if self.params.db_type == DbType.SQLLITE:
            repo = ReceiptComponentSqlLite(entity, self.db_access, drop_if_exists)
        else:
            repo = ReceiptComponentInMemory(entity, self.db_access, drop_if_exists)

        initializer.init(repo)
        return repo


# tests

# formatting (is 6 warning)
