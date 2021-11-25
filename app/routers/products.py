import uuid
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fractal.contrib.fastapi.routers.tokens import get_payload
from fractal.contrib.tokens.models import TokenPayload
from fractal.core.specifications.account_id_specification import AccountIdSpecification
from fractal.core.specifications.id_specification import IdSpecification
from pydantic import BaseModel

from app.routers import Routes
from app.service.domain.products import Product
from app.service.main import ProductFractal

router = APIRouter()
fractal = ProductFractal()


class ProductContract(BaseModel):
    name: str
    price: Decimal

    def to_product(self, *, account_id: UUID, product_id: Optional[UUID] = None):
        return Product(
            id=str(product_id) if product_id else str(uuid.uuid4()),
            account_id=str(account_id),
            **self.dict()
        )


@router.post(
    Routes.PRODUCTS, response_model=Product, status_code=status.HTTP_201_CREATED
)
def add_product(
    product: ProductContract, payload: TokenPayload = Depends(get_payload(fractal))
):
    return fractal.context.product_repository.add(
        product.to_product(account_id=payload.account)
    )


@router.get(
    Routes.PRODUCTS, response_model=List[Product], status_code=status.HTTP_200_OK
)
def products(payload: TokenPayload = Depends(get_payload(fractal))):
    return list(
        fractal.context.product_repository.find(
            AccountIdSpecification(str(payload.account))
        )
    )


@router.get(Routes.PRODUCT, response_model=Product, status_code=status.HTTP_200_OK)
def product(product_id: UUID, payload: TokenPayload = Depends(get_payload(fractal))):
    return fractal.context.product_repository.find_one(
        AccountIdSpecification(str(payload.account)).And(
            IdSpecification(str(product_id))
        )
    )


@router.put(Routes.PRODUCT, response_model=Product, status_code=status.HTTP_200_OK)
def update_product(
    product_id: UUID,
    product: ProductContract,
    payload: TokenPayload = Depends(get_payload(fractal)),
):
    return fractal.context.product_repository.update(
        product.to_product(account_id=payload.account, product_id=product_id)
    )


@router.delete(Routes.PRODUCT, response_model=str, status_code=status.HTTP_200_OK)
def delete_product(
    product_id: UUID, payload: TokenPayload = Depends(get_payload(fractal))
):
    fractal.context.product_repository.remove_one(
        AccountIdSpecification(str(payload.account)).And(
            IdSpecification(str(product_id))
        )
    )
    return "ok"
