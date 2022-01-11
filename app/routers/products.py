import uuid
from decimal import Decimal
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel

from app import fractal
from app.routers import Routes
from app.service.domain.products import Product
from fractal.contrib.fastapi.routers.default import (
    DefaultRestRouterService,
    inject_default_rest_routes,
)


class ProductContract(BaseModel):
    name: str
    price: Decimal

    def to_entity(self, *, account_id: UUID, **kwargs):
        if "id" in kwargs:
            return Product(
                id=str(kwargs["id"]), account_id=str(account_id), **self.dict()
            )
        return Product(account_id=str(account_id), **self.dict())


class CreateProductContract(ProductContract):
    id: Optional[str] = None

    def to_entity(self, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        return super(CreateProductContract, self).to_entity(**kwargs)


class ProductRouterService(DefaultRestRouterService):
    domain_entity_class = Product
    entities_route = Routes.PRODUCTS
    entity_route = Routes.PRODUCT
    entity_contract = ProductContract
    create_entity_contract = CreateProductContract

    def __init__(self):
        self.product_service = fractal.context.product_service

    def add_entity(
        self,
        contract: CreateProductContract,
        **kwargs,
    ):
        try:
            uuid.UUID(contract.id)
        except (ValueError, TypeError):
            contract.id = None
        _entity = contract.to_entity(
            user_id=kwargs.get("sub"), account_id=kwargs.get("account")
        )
        return self.product_service.add(_entity, str(kwargs.get("sub")))

    def find_entities(
        self,
        q: str = "",
        **kwargs,
    ):
        return self.product_service.find(str(kwargs.get("account")), q)

    def get_entity(
        self,
        entity_id: UUID,
        **kwargs,
    ):
        return self.product_service.get(str(entity_id), str(kwargs.get("account")))

    def update_entity(
        self,
        entity_id: UUID,
        contract: ProductContract,
        **kwargs,
    ):
        _entity = contract.to_entity(
            id=entity_id, user_id=kwargs.get("sub"), account_id=kwargs.get("account")
        )
        return self.product_service.update(
            str(entity_id), _entity, str(kwargs.get("sub"))
        )

    def delete_entity(
        self,
        entity_id: UUID,
        **kwargs,
    ) -> Dict:
        self.product_service.delete(
            str(entity_id), str(kwargs.get("sub")), str(kwargs.get("account"))
        )
        return {}


router = inject_default_rest_routes(
    fractal,
    router_service_class=ProductRouterService,
    roles=dict(
        add=["user"],
        update=["user"],
        delete=["user"],
    ),
)
