from sqlite3 import Connection
from typing import Any, List

from app.infra.memory.database_management.database_factory import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity


class ReceiptComponentSqlLite:
    def __init__(
        self, entity: Entity, db_access: IDatabaseAccessObject, drop_if_exists: bool
    ):
        self._entity = entity
        self._connection: Connection = db_access.get_access_object()

        if drop_if_exists:
            cursor = self._connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS " + self._entity.name)
            self._connection.commit()

        cursor = self._connection.cursor()
        cursor.execute(self._entity.to_sql_representation())
        self._connection.commit()
        cursor.close()

    def initialize_with_items(self, items: List[Any]) -> None:
        pass

    def add_receipt_component(self, receipt_id: int, product_ids: List[int]) -> None:
        for i in product_ids:
            cursor = self._connection.cursor()
            cursor.execute(
                "INSERT INTO "
                + self._entity.name
                + " (receipt_id, product_id) values (?,?)",
                [receipt_id, i],
            )
            cursor.close()

    def get_receipt_component(self, receipt_id: int) -> List[int]:
        result = []
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM " + self._entity.name + " WHERE receipt_id = ? ",
            [receipt_id],
        )
        data = cursor.fetchall()
        for i in data:
            result.append(int(i[2]))
        cursor.close()
        return result
