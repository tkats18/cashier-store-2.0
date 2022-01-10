from typing import List, Protocol

from app.core.product.product_representation import ProductFullRepresentation


class IProductDb(Protocol):
    def get_product_by_ids_in(
        self, product_ids: List[int]
    ) -> List[ProductFullRepresentation]:
        pass

    def get_all_products(self) -> List[ProductFullRepresentation]:
        pass
