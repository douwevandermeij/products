from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app import fractal
from app.routers import Routes
from app.service.domain.commands.products.add import AddProductCommand
from app.service.domain.commands.products.delete import DeleteProductCommand
from app.service.domain.commands.products.update import UpdateProductCommand
from app.service.domain.products import Product
from fractal.contrib.fastapi.routers.default import inject_default_rest_routes


class ProductContract(BaseModel):
    name: str
    price: Decimal

    def to_entity(self, *, account_id: UUID, **kwargs):
        if "id" in kwargs:
            return Product(
                id=str(kwargs["id"]), account_id=str(account_id), **self.dict()
            )
        return Product(account_id=str(account_id), **self.dict())


router = inject_default_rest_routes(
    fractal,
    domain_entity_class=Product,
    entities_route=Routes.PRODUCTS,
    entity_route=Routes.PRODUCT,
    entity_repository_name="product_repository",
    entity_contract=ProductContract,
    search_fields=["name"],
    add_entity_command=AddProductCommand,
    update_entity_command=UpdateProductCommand,
    delete_entity_command=DeleteProductCommand,
    roles=dict(
        add=["user"],
        update=["user"],
        delete=["user"],
    ),
)
