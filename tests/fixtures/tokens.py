from types import SimpleNamespace

import pytest


@pytest.fixture
def account():
    return SimpleNamespace(
        **{
            "id": "00000000-0000-0000-0000-000000000000",
        }
    )


@pytest.fixture
def user():
    return SimpleNamespace(
        **{
            "id": "00000000-0000-0000-0000-000000000000",
        }
    )


@pytest.fixture
def token(fractal, user, account):
    return fractal.context.token_service.generate(
        {
            "sub": user.id,
            "account": account.id,
            "roles": ["user"],
        }
    )


@pytest.fixture
def admin_token(fractal, user, account):
    return fractal.context.token_service.generate(
        {
            "sub": user.id,
            "account": account.id,
            "roles": ["admin"],
        }
    )
