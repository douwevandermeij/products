from dataclasses import dataclass

from app.service.context import ApplicationContext
from app.service.domain.products import Product, ProductRepository
from fractal.core.command_bus.command_handler import CommandHandler
from fractal.core.command_bus.commands import DeleteEntityCommand


@dataclass
class DeleteProductCommand(DeleteEntityCommand[Product]):
    pass


class DeleteProductCommandHandler(CommandHandler):
    command = DeleteProductCommand

    def __init__(
        self,
        product_repository: ProductRepository,
    ):
        self.product_repository = product_repository

    @staticmethod
    def install(context: ApplicationContext):
        context.command_bus.add_handler(
            DeleteProductCommandHandler(
                context.product_repository,
            )
        )

    def handle(self, command: DeleteProductCommand):
        self.product_repository.remove_one(
            command.specification,
        )
