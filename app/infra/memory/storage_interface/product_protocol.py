from typing import List

from app.core.product.product_representation import ProductFullRepresentation
from app.infra.memory.storage_interface.initializing_storage import InitializingStorage


class IProductDb(InitializingStorage):  # type: ignore
    def get_product_by_ids_in(
        self, product_ids: List[int]
    ) -> List[ProductFullRepresentation]:
        pass

    def get_all_products(self) -> List[ProductFullRepresentation]:
        pass
