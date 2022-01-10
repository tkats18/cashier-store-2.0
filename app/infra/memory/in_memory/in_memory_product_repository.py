from typing import List

from app.core.product.product_representation import ProductFullRepresentation
from app.infra.memory.database_management.database_factory import IDatabaseAccessObject
from app.infra.memory.entity_management.entity_builder import Entity


class ProductInMemory:
    def __init__(
        self, entity: Entity, db_access: IDatabaseAccessObject, drop_if_exists: bool
    ):
        self.drop_if_exists = drop_if_exists
        self.entity = entity
        self.db_access = db_access

    def get_product_by_ids_in(
        self, product_ids: List[int]
    ) -> List[ProductFullRepresentation]:
        raise NotImplementedError()

    def get_all_products(self) -> List[ProductFullRepresentation]:
        raise NotImplementedError()
