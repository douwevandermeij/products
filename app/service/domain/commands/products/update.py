from dataclasses import dataclass

from app.service.context import ApplicationContext
from app.service.domain.products import Product, ProductRepository
from fractal.core.command_bus.command_handler import CommandHandler
from fractal.core.command_bus.commands import UpdateEntityCommand


@dataclass
class UpdateProductCommand(UpdateEntityCommand[Product]):
    pass


class UpdateProductCommandHandler(CommandHandler):
    command = UpdateProductCommand

    def __init__(
        self,
        product_repository: ProductRepository,
    ):
        self.product_repository = product_repository

    @staticmethod
    def install(context: ApplicationContext):
        context.command_bus.add_handler(
            UpdateProductCommandHandler(
                context.product_repository,
            )
        )

    def handle(self, command: UpdateProductCommand):
        self.product_repository.update(command.entity)
