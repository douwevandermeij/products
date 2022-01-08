import json
import uuid

from app.routers import Routes


def test_add_product(client, fractal, token, product):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert len(list(fractal.context.product_repository.find())) == 1


def test_add_product_no_id(client, fractal, token, product):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    data = product.__dict__
    del data["id"]
    response = client.post(
        Routes.PRODUCTS,
        data=json.dumps(data, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    uuid.UUID(response.json()["id"])
    assert len(list(fractal.context.product_repository.find())) == 1


def test_get_products(client, fractal, token, product, another_product):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        Routes.PRODUCTS,
        data=json.dumps(another_product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        Routes.PRODUCTS,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2


def test_get_products_filter(client, fractal, token, product, another_product):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        Routes.PRODUCTS,
        data=json.dumps(another_product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        Routes.PRODUCTS,
        params=dict(q="another"),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1


def test_get_product(client, fractal, token, product):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        Routes.PRODUCT.format(entity_id=product.id),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data == product.asdict()


def test_get_product_not_found(client, fractal, token, product):
    response = client.get(
        Routes.PRODUCT.format(entity_id=product.id),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
    assert response.json()["code"] == "PRODUCT_NOT_FOUND"


def test_update_product(client, fractal, token, product):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    product.name = "changed"

    response = client.put(
        Routes.PRODUCT.format(entity_id=product.id),
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data == product.asdict()


def test_delete_product(client, fractal, token, product):
    from fractal.core.utils.json_encoder import EnhancedEncoder

    client.post(
        Routes.PRODUCTS,
        data=json.dumps(product.__dict__, cls=EnhancedEncoder),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.delete(
        Routes.PRODUCT.format(entity_id=product.id),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    response = client.get(
        Routes.PRODUCT.format(entity_id=product.id),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
