from fractal.core.repositories.inmemory_repository_mixin import InMemoryRepositoryMixin
from fractal.core.specifications.generic.specification import Specification

from app.service.adapters.utils import FirestoreRepositoryDictMixin
from app.service.domain.products import (
    Product,
    ProductNotFoundException,
    ProductRepository,
)


class InMemoryProductRepository(ProductRepository, InMemoryRepositoryMixin[Product]):
    def find_one(self, specification: Specification) -> Product:
        obj = super(InMemoryProductRepository, self).find_one(specification)
        if not obj:
            raise ProductNotFoundException
        return obj


class FirestoreProductRepository(
    ProductRepository, FirestoreRepositoryDictMixin[Product]
):
    pass
