import json
from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from app.core.product.product_representation import ProductRepresentation
from app.infra.memory.storage_interface.initializing_storage import InitializingStorage


class IEntityInitializer(Protocol):
    def init(self, initializer_storage: InitializingStorage) -> None:
        pass


class BaseEntityInitializer(IEntityInitializer):
    @abstractmethod
    def init(self, initializer_storage: InitializingStorage) -> None:
        pass

    def __call__(self, initializer_storage: InitializingStorage) -> None:
        return self.init(initializer_storage)


@dataclass
class ProductFileInitializer(BaseEntityInitializer):
    file_path: str

    def init(self, initializer_storage: InitializingStorage) -> None:
        f = open(self.file_path)
        data = json.load(f)

        product_arr = []
        for i in data["products"]:
            product_arr.append(
                ProductRepresentation(
                    name=i["name"], units=i["units"], price=float(i["price"])
                )
            )

        initializer_storage.initialize_with_items(product_arr)


class EmptyFileInitializer(BaseEntityInitializer):
    def init(self, initializer_storage: InitializingStorage) -> None:
        return
