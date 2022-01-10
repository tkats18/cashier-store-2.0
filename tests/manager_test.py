from app.core.product.product_interactor import ProductInteractor
from app.core.receipt.receipt_interactor import ReceiptInteractor
from app.core.receipt.receipt_models import FillReceipt
from app.core.report.report_interactor import ReportInteractor
from app.core.report.report_model import ReportType
from app.core.report.report_strategy import XReportStrategy
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

receipt_repository = conf.receipt_repository(
    receipt_entity,
    EmptyFileInitializer(),
    True,
)
receipt_interactor = ReceiptInteractor(
    receipt_repository, receipt_component_repository, product_interactor
)


# def _to_st()
def test_manager_basic() -> None:
    report_engines = dict({ReportType.X_REPORT: XReportStrategy()})
    report_interactor = ReportInteractor(receipt_interactor, report_engines)
    # 2022 - 01 - 10
    product_ids = []
    products = product_interactor.get_products_by_ids_in(None)

    for i in products.get_products().response:
        product_ids.append(i.product_id)

    rec_1 = receipt_interactor.open_receipt()
    rec_2 = receipt_interactor.open_receipt()
    rec_3 = receipt_interactor.open_receipt()

    receipt_interactor.add_items_to_receipt(FillReceipt(rec_1.receipt_id, product_ids))
    receipt_interactor.add_items_to_receipt(FillReceipt(rec_2.receipt_id, product_ids))
    receipt_interactor.add_items_to_receipt(FillReceipt(rec_3.receipt_id, product_ids))

    receipt_interactor.close_receipt(rec_1.receipt_id)
    receipt_interactor.close_receipt(rec_2.receipt_id)
    report = report_interactor.generate_report(
        ReportType.X_REPORT,
        receipt_interactor.get_receipt(rec_1.receipt_id).receipt.create_time,
    )
    assert report.response["closed"] == 2
    receipt_interactor.close_receipt(rec_3.receipt_id)

    report = report_interactor.generate_report(
        ReportType.X_REPORT,
        receipt_interactor.get_receipt(rec_1.receipt_id).receipt.create_time,
    )
    assert report.response["revenue"] == products.calculate_total_price() * 3
    assert report.response["closed"] == 3
    assert report.response["items_sold"][0].sold == 3
