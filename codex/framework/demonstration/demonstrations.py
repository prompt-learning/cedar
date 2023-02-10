from abc import ABC, abstractmethod


class Demonstration(ABC):

    def __init__(self, with_commands):
        self.with_commands = with_commands

    @abstractmethod
    def construct(self):
        pass
