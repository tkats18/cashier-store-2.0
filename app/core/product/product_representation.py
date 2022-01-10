from dataclasses import dataclass
from typing import List, Protocol


@dataclass
class ProductRepresentation:
    name: str
    units: int
    price: float


@dataclass
class ProductFullRepresentation(ProductRepresentation):
    product_id: int


@dataclass
class ProductListResponse:
    response: List[ProductFullRepresentation]


class IProducts(Protocol):
    def get_products(self) -> ProductListResponse:
        pass

    def calculate_total_price(self) -> float:
        pass


class Product:
    def __init__(self, product_id: int, name: str, units: int, price: float):
        self.product_id = product_id
        self.name = name
        self.units = units
        self.price = price

    def calculate_total_price(self) -> float:
        return self.price * self.units

    def get_products(self) -> ProductListResponse:
        return ProductListResponse(
            [
                ProductFullRepresentation(
                    self.name, self.units, self.price, self.product_id
                )
            ]
        )


class ProductComposite:
    def __init__(self, products: List[Product]):
        self.products = products

    def calculate_total_price(self) -> float:
        return sum(i.calculate_total_price() for i in self.products)

    def get_products(self) -> ProductListResponse:
        result = []
        for i in self.products:
            result.append(i.get_products().response[0])
        return ProductListResponse(result)
