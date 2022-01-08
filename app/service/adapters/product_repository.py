from app.service.domain.products import Product, ProductRepository
from fractal.contrib.gcp.firestore.repositories import FirestoreRepositoryDictMixin
from fractal.core.repositories.inmemory_repository_mixin import InMemoryRepositoryMixin


class InMemoryProductRepository(ProductRepository, InMemoryRepositoryMixin[Product]):
    pass


class FirestoreProductRepository(
    ProductRepository, FirestoreRepositoryDictMixin[Product]
):
    pass
