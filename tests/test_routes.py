import json

from app.routers import Routes


def test_add_product(client, product, token):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201


def test_add_product_no_id(client, product, token):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    product.__dict__.pop("id")
    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201


def test_get_products(fractal, client, product, token):
    from fractal.contrib.tokens.services import DummyJsonTokenService
    from fractal.core.utils.json_encoder import EnhancedEncoder

    fractal.context.token_service = DummyJsonTokenService()

    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    response = client.get(Routes.PRODUCTS, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == product.id


def test_get_product(fractal, client, product, token):
    from fractal.contrib.tokens.services import DummyJsonTokenService
    from fractal.core.utils.json_encoder import EnhancedEncoder

    fractal.context.token_service = DummyJsonTokenService()

    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    response = client.get(
        Routes.PRODUCT.format(product_id=product.id),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == product.id


def test_update_product(fractal, client, product, token):
    from fractal.contrib.tokens.services import DummyJsonTokenService
    from fractal.core.utils.json_encoder import EnhancedEncoder

    fractal.context.token_service = DummyJsonTokenService()

    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    product.name = "update"
    response = client.put(
        Routes.PRODUCT.format(product_id=product.id),
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == product.name


def test_delete_product(fractal, client, product, token):
    from fractal.contrib.tokens.services import DummyJsonTokenService
    from fractal.core.utils.json_encoder import EnhancedEncoder

    fractal.context.token_service = DummyJsonTokenService()

    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    response = client.delete(
        Routes.PRODUCT.format(product_id=product.id),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    response = client.get(
        Routes.PRODUCT.format(product_id=product.id),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
