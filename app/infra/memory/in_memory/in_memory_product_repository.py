from typing import List

from app.core.product.product_representation import ProductFullRepresentation
from app.infra.memory.database_management.database_factory import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity
from app.infra.memory.sql_lite.sql_lite_product_repository import IProductDb


class ProductInMemory(IProductDb):  # type: ignore
    def __init__(
        self, entity: Entity, db_access: IDatabaseAccessObject, drop_if_exists: bool
    ):
        self.entity = entity
        self.db_access = db_access

    def get_product_by_ids_in(
        self, product_ids: List[int]
    ) -> List[ProductFullRepresentation]:
        raise NotImplementedError()

    def get_all_products(self) -> List[ProductFullRepresentation]:
        raise NotImplementedError()
