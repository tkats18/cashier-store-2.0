from fastapi import FastAPI

from app.core.facade import StoreAdapter
from app.core.store.store import StoreService
from app.infra.fastapi.routers import cashier, customer, manager
from app.infra.memory.database_management.database_config import (
    DbConfigurationParams,
    DbCreationParams,
    DbType,
)
from app.infra.memory.database_management.database_factory import DatabaseConfiguration
from app.infra.memory.entity_management.entity_builder import EntityBuilder
from app.infra.memory.entity_management.entity_enum import DbEntityEnum
from app.infra.memory.entity_management.entity_init_startegy import (
    EmptyFileInitializer,
    ProductFileInitializer,
)


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(cashier.cashier_api)
    app.include_router(customer.customer_api)
    app.include_router(manager.manager_api)

    product_entity = (
        EntityBuilder()
        .with_name(DbEntityEnum.PRODUCT.name)
        .with_field("id", "integer primary key")
        .with_field("name", "varchar(50)")
        .with_field("price", "numeric")
        .with_field("pack_size", "integer")
        .build()
    )

    receipt_entity = (
        EntityBuilder()
        .with_name(DbEntityEnum.RECEIPT.name)
        .with_field("id", "integer primary key")
        .with_field("closed", "integer default 0")
        .with_field("creation_date", "varchar(50)")
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
            DbType.SQLLITE, DbConfigurationParams("./../infra/memory/sql_lite/data.db")
        )
    )
    product_repository = conf.product_repository(
        product_entity,
        ProductFileInitializer("./../../data_initial/products.json"),
        True,
    )
    receipt_repository = conf.receipt_repository(
        receipt_entity, EmptyFileInitializer(), True
    )
    receipt_component_repository = conf.receipt_component_repository(
        receipt_component_entity, EmptyFileInitializer(), True
    )

    store_service = StoreService.create(
        receipt_repository, product_repository, receipt_component_repository
    )
    app.state.core = StoreAdapter(store_service)

    return app
