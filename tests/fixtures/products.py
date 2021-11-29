import uuid
from decimal import Decimal

import pytest


@pytest.fixture
def product(account):
    from app.service.domain.products import Product

    return Product(
        id=str(uuid.uuid4()),
        account_id=account.id,
        name="product",
        price=Decimal(1.99),
    )
