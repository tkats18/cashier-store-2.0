import datetime
from sqlite3 import Connection
from typing import Any, List

from app.core.receipt.receipt_representation import (
    ReceiptDataPartialListRepresentation,
    ReceiptRepresentation,
    ReceiptDataPartialRepresentation,
)
from app.infra.memory.database_management.database_factory import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity
from app.infra.memory.storage_interface.receipt_protocol import IReceiptDb


class ReceiptSqlLite(IReceiptDb):  # type: ignore
    def __init__(
        self, entity: Entity, db_access: IDatabaseAccessObject, drop_if_exists: bool
    ):
        self.entity = entity
        self._connection: Connection = db_access.get_access_object()

        if drop_if_exists:
            cursor = self._connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS " + self.entity.name)
            self._connection.commit()

        cursor = self._connection.cursor()
        cursor.execute(self.entity.to_sql_representation())
        self._connection.commit()
        cursor.close()

    def open_receipt(self) -> int:
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO " + self.entity.name + "(creation_date) VALUES (?)",
            [datetime.date.today()],
        )
        self._connection.commit()
        receipt_id = cursor.lastrowid
        cursor.close()

        return int(receipt_id)

    # TODO tu ar arsebobs error
    def close_receipt(self, receipt_id: int) -> None:
        cursor = self._connection.cursor()
        cursor.execute(
            "update " + self.entity.name + " set closed = True where id = ?",
            [receipt_id],
        )
        self._connection.commit()

    def initialize_with_items(self, items: List[Any]) -> None:
        pass

    # TODO tu ar arsebobs error
    def get_receipt(self, receipt_id: int) -> ReceiptRepresentation:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM " + self.entity.name + " WHERE id = ?", [receipt_id]
        )
        result = cursor.fetchone()
        if result is None:
            raise RuntimeError()

        return ReceiptRepresentation(
            int(
                result[0],
            ),
            bool(result[1]),
            str(result[2]),
        )

    def find_receipts_on_day(
        self, date_time_obj: str
    ) -> ReceiptDataPartialListRepresentation:
        result = []

        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM " + self.entity.name + " WHERE creation_date = ?",
            [date_time_obj],
        )
        data = cursor.fetchall()
        for i in data:
            result.append(
                ReceiptDataPartialRepresentation(
                    int(
                        i[0],
                    )
                )
            )
        return ReceiptDataPartialListRepresentation(result)
