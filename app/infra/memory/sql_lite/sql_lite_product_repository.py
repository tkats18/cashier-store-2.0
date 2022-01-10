from sqlite3 import Connection, Cursor
from typing import Any, List

from app.core.product.product_representation import (
    ProductFullRepresentation,
    ProductRepresentation,
)
from app.infra.memory.database_management.database_factory import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity
from app.infra.memory.storage_interface.product_protocol import IProductDb


class ProductSqlLite(IProductDb):  # type: ignore
    def __init__(
        self, entity: Entity, db_access: IDatabaseAccessObject, drop_if_exists: bool
    ):
        self.entity = entity
        self.connection: Connection = db_access.get_access_object()

        if drop_if_exists:
            cursor = self.connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS " + self.entity.name)
            self.connection.commit()

        cursor = self.connection.cursor()
        cursor.execute(self.entity.to_sql_representation())
        self.connection.commit()
        cursor.close()

    def initialize_with_items(self, items: List[Any]) -> None:
        products: List[ProductRepresentation] = items
        for i in products:
            self._add_product(i)

    # TODO tu ar arsebobs error
    def get_product_by_ids_in(
        self, product_ids: List[int]
    ) -> List[ProductFullRepresentation]:
        final_res = []
        for i in product_ids:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM " + self.entity.name + " WHERE id = ? ", [i])
            res = self._extract_result(cursor)
            cursor.close()
            final_res.append(res[0])

        return final_res

    def get_all_products(self) -> List[ProductFullRepresentation]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM " + self.entity.name)
        res = self._extract_result(cursor)

        cursor.close()
        return res

    def _extract_result(self, cursor: Cursor) -> List[ProductFullRepresentation]:
        result_set = cursor.fetchall()
        result = []

        for i in result_set:
            result.append(ProductFullRepresentation(i[1], i[3], i[2], i[0]))

        return result

    def _add_product(self, product: ProductRepresentation) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO "
            + self.entity.name
            + "(name, price, pack_size) values (?,?,?)",
            [product.name, product.price, product.units],
        )
        cursor.close()
