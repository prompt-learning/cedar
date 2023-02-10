from abc import ABC, abstractmethod


class Prompt(ABC):

    @abstractmethod
    def construct_prompt(self):
        pass
