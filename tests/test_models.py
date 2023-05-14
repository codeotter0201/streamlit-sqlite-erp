from app.models import MyBase
import pytest

@pytest.fixture
def db():
    return MyBase("sqlite:///:memory:")

def test_create_product(db):
    product = db.product(
        id="00001",
        product_ts="2022-01-01 12:00:00",
        name="Product 1",
        color="紅",
        size="M",
    )
    assert product.id == "00001"
    assert str(product.product_ts) == "2022-01-01 12:00:00"
    assert product.name == "Product 1"
    assert product.color == "紅"
    assert product.size == "M"

def test_create_detail(db):
    product = db.product(
        id="00001",
        product_ts="2022-01-01 12:00:00",
        name="Product 1",
        color="紅",
        size="M",
    )
    db_session = db.Session()
    db_session.add(product)
    db_session.commit()

    detail = db.detail(
        id="00001",
        detail_ts="2022-01-01 13:00:00",
        quantity=10,
        price=100.0,
        type="進貨",
        supplier="供應商 A",
        note="備註",
    )
    db_session.add(detail)
    db_session.commit()

    assert detail.id == "00001"
    assert str(detail.detail_ts) == "2022-01-01 13:00:00"
    assert detail.quantity == 10
    assert detail.price == 100.0
    assert detail.type == "進貨"
    assert detail.supplier == "供應商 A"
    assert detail.note == "備註"
