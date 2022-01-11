from fractal.core.command_bus.command_bus import CommandBus
from fractal.core.repositories.filter_repository_mixin import FilterRepositoryMixin
from fractal.core.services import Service
from fractal.core.specifications.account_id_specification import AccountIdSpecification
from fractal.core.specifications.id_specification import IdSpecification

from app.service.context import ApplicationContext
from app.service.domain.products import Product, ProductRepository
from app.service.domain.products.commands.add import AddProductCommand
from app.service.domain.products.commands.delete import DeleteProductCommand
from app.service.domain.products.commands.update import UpdateProductCommand


class ProductService(Service):
    def __init__(
        self,
        command_bus: CommandBus,
        product_repository: ProductRepository,
    ):
        self.command_bus = command_bus
        self.product_repository = product_repository
        self.search_fields = ["name"]
        self.search_pre_processor = lambda i: i.lower()

    @classmethod
    def install(cls, context: ApplicationContext):
        yield cls(
            command_bus=context.command_bus,
            product_repository=context.product_repository,
        )

    def add(
        self,
        entity: Product,
        user_id: str,
    ):
        self.command_bus.handle(
            AddProductCommand(
                user_id=user_id,
                entity=entity,
            ),
        )
        return entity

    def find(
        self,
        account_id: str,
        q: str = "",
    ):
        if issubclass(self.product_repository.__class__, FilterRepositoryMixin):
            return list(
                self.product_repository.find_filter(
                    q,
                    fields=self.search_fields,
                    specification=AccountIdSpecification(account_id),
                    pre_processor=self.search_pre_processor,
                )
            )
        else:
            return list(
                self.product_repository.find(AccountIdSpecification(account_id))
            )

    def get(
        self,
        entity_id: str,
        account_id: str,
    ):
        return self.product_repository.find_one(
            AccountIdSpecification(account_id).And(IdSpecification(entity_id))
        )

    def update(
        self,
        entity_id: str,
        entity: Product,
        user_id: str,
    ):
        self.command_bus.handle(
            UpdateProductCommand(
                id=entity_id,
                entity=entity,
                user_id=user_id,
            ),
        )
        return entity

    def delete(
        self,
        entity_id: str,
        user_id: str,
        account_id: str,
    ):
        self.command_bus.handle(
            DeleteProductCommand(
                specification=AccountIdSpecification(account_id).And(
                    IdSpecification(entity_id)
                ),
                user_id=user_id,
            ),
        )
