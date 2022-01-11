from fractal.contrib.gcp.firestore.repositories import FirestoreRepositoryDictMixin
from fractal.core.repositories.inmemory_repository_mixin import InMemoryRepositoryMixin

from app.service.domain.products import Product, ProductRepository


class InMemoryProductRepository(ProductRepository, InMemoryRepositoryMixin[Product]):
    pass


class FirestoreProductRepository(
    ProductRepository, FirestoreRepositoryDictMixin[Product]
):
    pass
