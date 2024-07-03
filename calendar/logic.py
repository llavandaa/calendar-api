from datetime import date
import uuid

class CalendarLogic:
    def __init__(self, storage):
        self.storage = storage

    def create(self, event):
        if any(e.date == event.date for e in self.storage.list()):
            raise Exception(f"Событие на дату {event.date} уже существует")
        event.id = str(uuid.uuid4())
        self.storage.create(event)
        return event.id

    def list(self):
        return self.storage.list()

    def read(self, _id):
        return self.storage.read(_id)

    def update(self, _id, event):
        if any(e.date == event.date and e.id != _id for e in self.storage.list()):
            raise Exception(f"Событие на дату {event.date} уже существует")
        event.id = _id
        self.storage.update(event)

    def delete(self, _id):
        self.storage.delete(_id)
