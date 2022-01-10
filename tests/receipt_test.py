from app.core.model.store_exception import StoreException
from app.core.product.product_interactor import ProductInteractor
from app.core.receipt.receipt_interactor import ReceiptInteractor
from app.infra.memory.database_management.database_config import (
    DbCreationParams,
    DbType,
    DbConfigurationParams,
)
from app.infra.memory.database_management.database_factory import DatabaseConfiguration
from app.infra.memory.entity_management.entity_builder import EntityBuilder
from app.infra.memory.entity_management.entity_enum import DbEntityEnum
from app.infra.memory.entity_management.entity_init_startegy import (
    EmptyFileInitializer,
    ProductFileInitializer,
)

receipt_entity = (
    EntityBuilder()
    .with_name(DbEntityEnum.RECEIPT.name)
    .with_field("id", "integer primary key")
    .with_field("closed", "integer default 0")
    .with_field("creation_date", "varchar(50)")
    .build()
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

receipt_component_entity = (
    EntityBuilder()
    .with_name(DbEntityEnum.RECEIPT_COMPONENT.name)
    .with_field("id", "integer primary key")
    .with_field("receipt_id", "integer")
    .with_field("product_id", "integer")
    .build()
)

conf = DatabaseConfiguration(
    DbCreationParams(
        DbType.SQLLITE, DbConfigurationParams("../app/infra/memory/sql_lite/test.db")
    )
)
receipt_component_repository = conf.receipt_component_repository(
    receipt_component_entity, EmptyFileInitializer(), True
)

product_repository = conf.product_repository(
    product_entity,
    ProductFileInitializer("../data_initial/products.json"),
    True,
)
product_interactor = ProductInteractor(product_repository)


def test_receipt_basic() -> None:
    receipt_repository = conf.receipt_repository(
        receipt_entity,
        EmptyFileInitializer(),
        True,
    )
    ReceiptInteractor(
        receipt_repository, receipt_component_repository, product_interactor
    )


def test_receipt_simple() -> None:
    receipt_repository = conf.receipt_repository(
        receipt_entity,
        EmptyFileInitializer(),
        True,
    )
    receipt_interactor = ReceiptInteractor(
        receipt_repository, receipt_component_repository, product_interactor
    )

    recp_1 = receipt_interactor.open_receipt()
    recp_2 = receipt_interactor.open_receipt()

    full_1 = receipt_interactor.get_receipt(recp_1.receipt_id)
    full_2 = receipt_interactor.get_receipt(recp_2.receipt_id)

    assert full_2.total == 0.0
    assert full_1.total == 0.0

    assert not full_1.receipt.closed
    assert not full_2.receipt.closed


def test_receipt_middle() -> None:
    receipt_repository = conf.receipt_repository(
        receipt_entity,
        EmptyFileInitializer(),
        True,
    )
    receipt_interactor = ReceiptInteractor(
        receipt_repository, receipt_component_repository, product_interactor
    )

    products = product_interactor.get_products_by_ids_in(None)
    product_ids = []
    for i in products.get_products().response:
        product_ids.append(i.product_id)

    recp_1 = receipt_interactor.open_receipt()
    receipt_component_repository.add_receipt_component(recp_1.receipt_id, product_ids)
    fill_recp = receipt_interactor.get_receipt(recp_1.receipt_id)

    assert fill_recp.total == products.calculate_total_price()
    assert len(fill_recp.items.response) == len(products.get_products().response)


def test_receipt_hard() -> None:
    receipt_repository = conf.receipt_repository(
        receipt_entity,
        EmptyFileInitializer(),
        True,
    )
    receipt_interactor = ReceiptInteractor(
        receipt_repository, receipt_component_repository, product_interactor
    )

    products = product_interactor.get_products_by_ids_in(None)
    product_ids = []
    for i in products.get_products().response:
        product_ids.append(i.product_id)

    recp_1 = receipt_interactor.open_receipt()
    receipt_component_repository.add_receipt_component(recp_1.receipt_id, product_ids)
    receipt_interactor.close_receipt(recp_1.receipt_id)

    try:
        receipt_component_repository.add_receipt_component(
            recp_1.receipt_id, product_ids
        )
    except StoreException:
        assert len(
            receipt_interactor.get_receipt(recp_1.receipt_id).items.response
        ) == len(product_ids)
