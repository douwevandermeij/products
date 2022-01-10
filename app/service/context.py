from typing import Optional

from app.service.settings import Settings
from fractal.core.utils.application_context import ApplicationContext as BaseContext


class ApplicationContext(BaseContext):
    def load_repositories(self):
        from google.cloud.firestore_v1 import Client

        self.firestore_client: Optional[Client] = None

        def get_firestore_client():
            if not self.firestore_client:
                import firebase_admin
                from firebase_admin import firestore

                cred = None
                if service_account_key := Settings().GCP_SERVICE_ACCOUNT_KEY:
                    from firebase_admin import credentials

                    cred = credentials.Certificate(service_account_key)

                firebase_admin.initialize_app(cred)
                self.firestore_client = firestore.client()
            return self.firestore_client

        from app.service.domain.products import ProductRepository

        if Settings().PRODUCT_REPOSITORY_BACKEND == "firestore":
            from app.service.adapters.product_repository import (
                FirestoreProductRepository,
            )

            self.product_repository: ProductRepository = self.install_repository(
                FirestoreProductRepository(get_firestore_client()),
            )
        else:
            from app.service.adapters.product_repository import (
                InMemoryProductRepository,
            )

            self.product_repository: ProductRepository = self.install_repository(
                InMemoryProductRepository(),
            )

        if Settings().EVENT_STORE_BACKEND == "firestore":
            from fractal.contrib.gcp.firestore.event_store import (
                FirestoreEventStoreRepository,
            )
            from fractal.core.event_sourcing.event_store import EventStoreRepository

            self.event_store_repository: EventStoreRepository = (
                FirestoreEventStoreRepository(get_firestore_client())
            )

            from app.service.domain.products import events as product_events
            from fractal.contrib.fastapi.utils.json_encoder import (
                BaseModelEnhancedEncoder,
            )
            from fractal.core.event_sourcing.event_store import (
                EventStore,
                JsonEventStore,
            )

            self.event_store: EventStore = JsonEventStore(
                event_store_repository=self.event_store_repository,
                events=product_events.get_all(),
                json_encoder=BaseModelEnhancedEncoder,
            )
        else:
            from fractal.core.event_sourcing.event_store import (
                EventStoreRepository,
                InMemoryEventStoreRepository,
            )

            self.event_store_repository: EventStoreRepository = (
                InMemoryEventStoreRepository()
            )

            from fractal.core.event_sourcing.event_store import (
                EventStore,
                ObjectEventStore,
            )

            self.event_store: EventStore = ObjectEventStore(
                event_store_repository=self.event_store_repository,
            )

    def load_internal_services(self):
        if not Settings().SECRET_KEY:
            from fractal.contrib.tokens.services import StaticTokenService

            self.token_service = StaticTokenService()
        else:
            from fractal.contrib.tokens.services import SymmetricJwtTokenService

            self.token_service = SymmetricJwtTokenService(
                issuer=Settings().APP_NAME,
                secret=Settings().SECRET_KEY,
            )

    def load_command_bus(self):
        super(ApplicationContext, self).load_command_bus()

        from app.service.domain.products.commands.add import AddProductCommandHandler
        from app.service.domain.products.commands.delete import (
            DeleteProductCommandHandler,
        )
        from app.service.domain.products.commands.update import (
            UpdateProductCommandHandler,
        )

        AddProductCommandHandler.install(self)
        UpdateProductCommandHandler.install(self)
        DeleteProductCommandHandler.install(self)

    def load_event_projectors(self):
        from app.service.domain.products.events import ProductEventCommandMapper
        from fractal.core.event_sourcing.projectors.command_bus_projector import (
            CommandBusProjector,
        )
        from fractal.core.event_sourcing.projectors.event_store_projector import (
            EventStoreProjector,
        )
        from fractal.core.event_sourcing.projectors.print_projector import (
            PrintEventProjector,
        )

        return [
            CommandBusProjector(
                lambda: self.command_bus,
                [
                    ProductEventCommandMapper(),
                ],
            ),
            EventStoreProjector(self.event_store),
            PrintEventProjector(),
        ]
