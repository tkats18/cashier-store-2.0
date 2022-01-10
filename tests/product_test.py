import json
from typing import List, Any

from app.core.product.product_interactor import ProductInteractor
from app.core.product.product_representation import ProductFullRepresentation
from app.infra.memory.database_management.database_config import (
    DbCreationParams,
    DbType,
    DbConfigurationParams,
)
from app.infra.memory.database_management.database_factory import DatabaseConfiguration
from app.infra.memory.entity_management.entity_builder import EntityBuilder
from app.infra.memory.entity_management.entity_enum import DbEntityEnum
from app.infra.memory.entity_management.entity_init_startegy import (
    ProductFileInitializer,
)

product_entity = (
    EntityBuilder()
    .with_name(DbEntityEnum.PRODUCT.name)
    .with_field("id", "integer primary key")
    .with_field("name", "varchar(50)")
    .with_field("price", "numeric")
    .with_field("pack_size", "integer")
    .build()
)

conf = DatabaseConfiguration(
    DbCreationParams(
        DbType.SQLLITE, DbConfigurationParams("../app/infra/memory/sql_lite/test.db")
    )
)


def test_basic() -> None:
    product_repository = conf.product_repository(
        product_entity,
        ProductFileInitializer("../data_initial/products.json"),
        True,
    )
    ProductInteractor(product_repository)


def test_products_methods_init() -> None:
    product_repository = conf.product_repository(
        product_entity,
        ProductFileInitializer("../data_initial/products.json"),
        True,
    )
    ProductInteractor(product_repository)

    f = open("../data_initial/products.json")
    data = json.load(f)

    arr: List[Any] = data["products"]

    all_products: List[
        ProductFullRepresentation
    ] = product_repository.get_all_products()

    assert len(arr) == len(all_products)


def test_products_methods_simple() -> None:
    product_repository = conf.product_repository(
        product_entity,
        ProductFileInitializer("../data_initial/products.json"),
        True,
    )
    interactor = ProductInteractor(product_repository)

    all_products: List[
        ProductFullRepresentation
    ] = product_repository.get_all_products()

    ids = []
    for q in all_products:
        ids.append(q.product_id)

    by_id_products = interactor.get_products_by_ids_in(ids)
    assert len(all_products) == len(by_id_products.get_products().response)


def test_products_methods_middle() -> None:
    product_repository = conf.product_repository(
        product_entity,
        ProductFileInitializer("../data_initial/products.json"),
        True,
    )
    interactor = ProductInteractor(product_repository)
    all_products: List[
        ProductFullRepresentation
    ] = product_repository.get_all_products()

    ids = []

    for q in all_products:
        ids.append(q.product_id)
    by_id_products = interactor.get_products_by_ids_in(ids)

    for i in all_products:
        found: bool = False
        for k in by_id_products.get_products().response:
            if (
                k.name == i.name
                and k.product_id == i.product_id
                and k.price == i.price
                and k.units == i.units
            ):
                found = True

        assert found


def test_products_methods_empty() -> None:
    product_repository = conf.product_repository(
        product_entity,
        ProductFileInitializer("../data_initial/products.json"),
        True,
    )
    interactor = ProductInteractor(product_repository)

    by_id_products = interactor.get_products_by_ids_in([])
    assert len(by_id_products.get_products().response) == 0
