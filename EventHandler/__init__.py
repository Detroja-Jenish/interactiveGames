import pygame
class Event:
    def __init__(self, type, *callbacks, condition=lambda _: True):
        self.type = type
        self.callbacks = callbacks
        self.condition = condition

class EventHandler:
    def __init__(self):
        self.registered_events = {}

    def registerEvent(self,event_name ,event):
        if event_name in self.registered_events:
            raise f"{event_name} event already exist."
        self.registered_events[event_name] = event


    def checkEventOccurnce(self):
        for event  in pygame.event.get():
            for name, registered_event in self.registered_events.items():
                if event.type == registered_event.type and registered_event.condition(event):
                    for callback in registered_event.callbacks:
                        callback(event)
                    break
