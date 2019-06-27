class Mediator:
    events = {}
    TYPES = {}

    def __init__(self, types):
        self.TYPES = types
        for key in self.TYPES.keys():
            self.events.update({ self.TYPES[key]: [] })
			
    def __del__(self):
        self.events.clear()			

    def getTypes(self):
        return self.TYPES				

    # подписаться на событие
    def subscribe(self, name, func):
        if name and func:
            self.events.get(name).append(func)

    # вызвать событие
    def call(self, name, data = None):
        cbs = self.events.get(name)
        if (cbs):
            for cb in cbs:
                cb(data)
						