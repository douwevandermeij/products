from dataclasses import asdict
from datetime import date
from decimal import Decimal

from fractal.contrib.gcp.firestore.repositories import FirestoreRepositoryMixin
from fractal.core.repositories import Entity


class FirestoreDict(dict):
    def __init__(self, obj):
        for i, v in enumerate(obj):
            if type(v[1]) is Decimal:
                obj[i] = (v[0], f"{v[1]:.2f}")
            if type(v[1]) is date:
                obj[i] = (v[0], v[1].isoformat())
        super(FirestoreDict, self).__init__(obj)


class FirestoreRepositoryDictMixin(FirestoreRepositoryMixin[Entity]):
    def add(self, entity: Entity) -> Entity:
        doc_ref = self.collection.document(entity.id)
        doc_ref.set(asdict(entity, dict_factory=FirestoreDict))
        return entity

    def update(self, entity: Entity, *, upsert=False) -> Entity:
        if not upsert:
            doc_ref = self.collection.document(entity.id)
            doc = doc_ref.get()
            if doc.exists:
                doc_ref.set(asdict(entity, dict_factory=FirestoreDict))
            return entity
        return self.add(entity)
