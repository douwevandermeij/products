from dataclasses import dataclass

from app.service.context import ApplicationContext
from app.service.domain.products import Product, ProductRepository
from fractal.core.command_bus.command_handler import CommandHandler
from fractal.core.command_bus.commands import AddEntityCommand


@dataclass
class AddProductCommand(AddEntityCommand[Product]):
    pass


class AddProductCommandHandler(CommandHandler):
    command = AddProductCommand

    def __init__(
        self,
        product_repository: ProductRepository,
    ):
        self.product_repository = product_repository

    @staticmethod
    def install(context: ApplicationContext):
        context.command_bus.add_handler(
            AddProductCommandHandler(
                context.product_repository,
            )
        )

    def handle(self, command: AddProductCommand):
        self.product_repository.add(command.entity)
