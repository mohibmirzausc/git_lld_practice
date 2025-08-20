from abc import ABC, abstractmethod
from typing import List, Optional

class SplitStrategy(ABC):

    @abstractmethod
    def calculate_dues(self, participants: List['Users'], split_values: Optional[List[float]]):
        pass

class EqualSplitStrategy(SplitStrategy):
    def calculate_dues(self, participants: List['Users'], split_values: Optional[List[float]]):
        
        
    
class PecentageSplitStrategy(SplitStrategy):

    def calculate_dues(self, participants: List['Users'], split_values: Optional[List[float]]):
        return "percentagesplit"


    
    