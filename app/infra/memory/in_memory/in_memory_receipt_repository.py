from typing import Any, List

from app.core.receipt.receipt_representation import (
    ReceiptDataPartialListRepresentation,
    ReceiptRepresentation,
)
from app.infra.memory.database_management.database_factory import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity
from app.infra.memory.sql_lite.sql_lite_receipt_repository import IReceiptDb


class ReceiptInMemory(IReceiptDb):  # type: ignore
    def __init__(
        self, entity: Entity, db_access: IDatabaseAccessObject, drop_if_exists: bool
    ):
        self.entity = entity
        self.db_access = db_access

    def open_receipt(self) -> None:
        raise NotImplementedError()

    def close_receipt(self, receipt_id: int) -> None:
        raise NotImplementedError()

    def initialize_with_items(self, items: List[Any]) -> None:
        raise NotImplementedError()

    def get_receipt(self, receipt_id: int) -> ReceiptRepresentation:
        raise NotImplementedError()

    def find_receipts_on_day(
        self, date_time_obj: str
    ) -> ReceiptDataPartialListRepresentation:
        raise NotImplementedError()
