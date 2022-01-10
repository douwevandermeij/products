from dataclasses import dataclass
from datetime import datetime

from app.service.context import ApplicationContext
from app.service.domain.products import Product, ProductRepository
from app.service.domain.products.events import ProductAddedEvent
from fractal.core.command_bus.command_handler import CommandHandler
from fractal.core.command_bus.commands import AddEntityCommand
from fractal.core.event_sourcing.event_publisher import EventPublisher


@dataclass
class AddProductCommand(AddEntityCommand[Product]):
    pass


class AddProductCommandHandler(CommandHandler):
    command = AddProductCommand

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
            AddProductCommandHandler(
                context.event_publisher,
                context.product_repository,
            )
        )

    def handle(self, command: AddProductCommand):
        event = ProductAddedEvent(
            id=command.entity.id,
            account_id=command.entity.account_id,
            name=command.entity.name,
            price=command.entity.price,
            created_by=command.user_id,
            created_on=datetime.utcnow(),
        )
        self.product_repository.add(command.entity)
        self.event_publisher.publish_event(event)
