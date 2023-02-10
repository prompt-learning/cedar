import json
from abc import ABC, abstractmethod


class Dataset(ABC):

    @abstractmethod
    def parse(self):
        pass
