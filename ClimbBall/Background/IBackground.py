from abc import ABC, abstractmethod


class IBackground(ABC):
    @abstractmethod
    def draw(self):
        pass