from sqlite3 import Connection, Cursor
from typing import Any, List

from app.core.model.store_exception import StoreException
from app.core.product.product_representation import (
    ProductFullRepresentation,
    ProductRepresentation,
)
from app.infra.memory.database_management.database_factory import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity


class ProductSqlLite:
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
        products: List[ProductRepresentation] = items
        for i in products:
            self._add_product(i)

    def get_product_by_ids_in(
        self, product_ids: List[int]
    ) -> List[ProductFullRepresentation]:
        final_res = []
        for i in product_ids:
            if not self._product_exists(i):
                raise StoreException("Product with id " + str(i) + " does not exist ")

            cursor = self._connection.cursor()
            cursor.execute("SELECT * FROM " + self._entity.name + " WHERE id = ? ", [i])
            res = self._extract_result(cursor)
            cursor.close()
            final_res.append(res[0])

        return final_res

    def get_all_products(self) -> List[ProductFullRepresentation]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM " + self._entity.name)
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
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO "
            + self._entity.name
            + "(name, price, pack_size) values (?,?,?)",
            [product.name, product.price, product.units],
        )
        cursor.close()

    def _product_exists(self, product_id: int) -> bool:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM " + self._entity.name + " WHERE id = ?);",
            [product_id],
        )
        product_exists = cursor.fetchone()
        cursor.close()
        return bool(product_exists[0])
