
from abc import ABCMeta, abstractmethod

class StatsAbc(metaclass=ABCMeta):

    @abstractmethod
    def get_stats(self, pDictionary:dict) -> dict:
        raise Exception("concrete class must implement get_stats")
