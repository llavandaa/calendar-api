import model

class Storage:
    def __init__(self):
        self.events = {}

    def create(self, event: model.Event):
        self.events[event.id] = event

    def list(self):
        return list(self.events.values())

    def read(self, _id: str):
        if _id in self.events:
            return self.events[_id]
        else:
            raise Exception("Event not found")

    def update(self, event: model.Event):
        if event.id in self.events:
            self.events[event.id] = event
        else:
            raise Exception("Event not found")

    def delete(self, _id: str):
        if _id in self.events:
            del self.events[_id]
        else:
            raise Exception("Event not found")
