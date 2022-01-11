from dataclasses import dataclass

from fractal.core.command_bus.command_handler import CommandHandler
from fractal.core.command_bus.commands import DeleteEntityCommand
from fractal.core.event_sourcing.event_publisher import EventPublisher

from app.service.context import ApplicationContext
from app.service.domain.products import Product, ProductRepository
from app.service.domain.products.events import ProductDeletedEvent


@dataclass
class DeleteProductCommand(DeleteEntityCommand[Product]):
    user_id: str


class DeleteProductCommandHandler(CommandHandler):
    command = DeleteProductCommand

    def __init__(
        self,
        event_publisher: EventPublisher,
        product_repository: ProductRepository,
    ):
        self.event_publisher = event_publisher
        self.product_repository = product_repository

    @staticmethod
    def install(context: ApplicationContext):
        context.command_bus.add_handler(
            DeleteProductCommandHandler(
                context.event_publisher,
                context.product_repository,
            )
        )

    def handle(self, command: DeleteProductCommand):
        product = self.product_repository.find_one(
            command.specification,
        )
        event = ProductDeletedEvent(
            id=product.id,
        )
        self.product_repository.remove_one(
            command.specification,
        )
        self.event_publisher.publish_event(event)
