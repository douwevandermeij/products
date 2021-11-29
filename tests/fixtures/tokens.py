import uuid
from types import SimpleNamespace

import pytest


@pytest.fixture
def account():
    return SimpleNamespace(
        **{
            "id": str(uuid.uuid4()),
        }
    )


@pytest.fixture
def user():
    return SimpleNamespace(
        **{
            "id": str(uuid.uuid4()),
        }
    )


@pytest.fixture
def token(fractal, user, account):
    return fractal.context.token_service.generate(
        {
            "sub": user.id,
            "account": account.id,
        }
    )
