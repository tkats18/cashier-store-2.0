from dataclasses import dataclass
from typing import List, Optional

from app.core.product.product_representation import IProducts, Product, ProductComposite
from app.infra.memory.storage_interface.product_protocol import IProductDb


@dataclass
class ProductInteractor:
    product_db: IProductDb

    def get_products_by_ids_in(self, ids: Optional[List[int]] = None) -> IProducts:
        if ids is None:
            product_representations = self.product_db.get_all_products()
        else:
            product_representations = self.product_db.get_product_by_ids_in(ids)

        products = []
        for i in product_representations:
            products.append(Product(i.product_id, i.name, i.units, i.price))

        return ProductComposite(products)
