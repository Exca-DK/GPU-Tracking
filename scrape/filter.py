from abc import ABC, abstractmethod
from dataclasses import dataclass

from scrape.content.GPU_Base_Data import BaseGPU

class BaseScraperFilter(ABC):

    @abstractmethod
    def ShouldKeep(self, item: BaseGPU) -> bool:
        pass

@dataclass
class LowerThanFilter(BaseScraperFilter):

    price: float = 10000000000.0

    def ShouldKeep(self, item: BaseGPU) -> bool:
        if item.price < self.price:
            return True
        return False

@dataclass
class HigherThanFilter(BaseScraperFilter):

    price: float = 0.0

    def ShouldKeep(self, item: BaseGPU) -> bool:
        if item.price > self.price:
            return True
        return False

@dataclass
class MinMaxFilter(BaseScraperFilter):

    priceMin: float = 0.0
    priceMax: float = 10000000000.0

    def ShouldKeep(self, item: BaseGPU) -> bool:
        if item.price < self.priceMax and item.price > self.priceMin:
            return True
        return False