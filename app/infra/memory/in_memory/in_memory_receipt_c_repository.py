from sqlite3 import Connection
from typing import List

from app.infra.memory.database_management.database_access import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity


class ReceiptComponentInMemory:
    def __init__(
        self, entity: Entity, db_access: IDatabaseAccessObject, drop_if_exists: bool
    ):
        self.drop_if_exists = drop_if_exists
        self.entity = entity
        self._connection: Connection = db_access.get_access_object()

    def add_receipt_component(self, receipt_id: int, product_ids: List[int]) -> None:
        raise NotImplementedError()

    def get_receipt_component(self, receipt_id: int) -> List[int]:
        raise NotImplementedError()
