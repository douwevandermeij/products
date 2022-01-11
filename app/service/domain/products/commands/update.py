from dataclasses import dataclass
from datetime import datetime

from app.service.context import ApplicationContext
from app.service.domain.products import Product, ProductRepository
from app.service.domain.products.events import ProductUpdatedEvent
from fractal.core.command_bus.command_handler import CommandHandler
from fractal.core.command_bus.commands import UpdateEntityCommand
from fractal.core.event_sourcing.event_publisher import EventPublisher


@dataclass
class UpdateProductCommand(UpdateEntityCommand[Product]):
    user_id: str


class UpdateProductCommandHandler(CommandHandler):
    command = UpdateProductCommand

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
            UpdateProductCommandHandler(
                context.event_publisher,
                context.product_repository,
            )
        )

    def handle(self, command: UpdateProductCommand):
        event = ProductUpdatedEvent(
            id=command.entity.id,
            account_id=command.entity.account_id,
            name=command.entity.name,
            price=command.entity.price,
            updated_by=command.user_id,
            updated_on=datetime.utcnow(),
        )
        self.product_repository.update(command.entity)
        self.event_publisher.publish_event(event)
