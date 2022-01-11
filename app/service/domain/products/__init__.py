from abc import ABC
from dataclasses import dataclass  # NOQA
from decimal import Decimal

from fractal.core.exceptions import DomainException
from fractal.core.models import Model
from fractal.core.repositories import Repository
from fractal.core.repositories.filter_repository_mixin import FilterRepositoryMixin
from pydantic.dataclasses import dataclass


@dataclass
class Product(Model):
    id: str
    account_id: str
    name: str
    price: Decimal


class ProductNotFoundException(DomainException):
    code = "PRODUCT_NOT_FOUND"
    status_code = 404

    def __init__(self, message=None):
        if not message:
            message = "Product not found!"
        super(ProductNotFoundException, self).__init__(message)


class ProductRepository(FilterRepositoryMixin[Product], Repository[Product], ABC):
    object_not_found_exception = ProductNotFoundException
