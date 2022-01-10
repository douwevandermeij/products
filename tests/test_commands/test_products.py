def test_add_product(fractal, product, user):
    from app.service.domain.products.commands.add import AddProductCommand

    fractal.context.command_bus.handle(
        AddProductCommand(entity=product, user_id=user.id)
    )

    assert len(fractal.context.event_store.get_event_stream().events) == 1
    from app.service.domain.products.events import ProductAddedEvent

    assert [
        type(event) for event in fractal.context.event_store.get_event_stream().events
    ] == [ProductAddedEvent]


def test_update_product(fractal, product, user):
    from app.service.domain.products.commands.add import AddProductCommand
    from app.service.domain.products.commands.update import UpdateProductCommand

    fractal.context.command_bus.handle(
        AddProductCommand(entity=product, user_id=user.id)
    )
    fractal.context.command_bus.handle(
        UpdateProductCommand(id=product.id, entity=product, user_id=user.id)
    )

    assert len(fractal.context.event_store.get_event_stream().events) == 2
    from app.service.domain.products.events import (
        ProductAddedEvent,
        ProductUpdatedEvent,
    )

    assert [
        type(event) for event in fractal.context.event_store.get_event_stream().events
    ] == [ProductAddedEvent, ProductUpdatedEvent]


def test_delete_product(fractal, product, user):
    from app.service.domain.products.commands.add import AddProductCommand
    from app.service.domain.products.commands.delete import DeleteProductCommand
    from fractal.core.specifications.id_specification import IdSpecification

    fractal.context.command_bus.handle(
        AddProductCommand(entity=product, user_id=user.id)
    )
    fractal.context.command_bus.handle(
        DeleteProductCommand(specification=IdSpecification(product.id), user_id=user.id)
    )

    assert len(fractal.context.event_store.get_event_stream().events) == 2
    from app.service.domain.products.events import (
        ProductAddedEvent,
        ProductDeletedEvent,
    )

    assert [
        type(event) for event in fractal.context.event_store.get_event_stream().events
    ] == [ProductAddedEvent, ProductDeletedEvent]
