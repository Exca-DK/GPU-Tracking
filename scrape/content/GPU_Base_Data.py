from dataclasses import dataclass
from datetime import datetime
from json import dumps

@dataclass(frozen=False)
class BaseGPU:
    distributor: str
    model: int
    price: str
   

@dataclass(frozen=False)
class ShopGPU:
    gpu_info: BaseGPU
    link: str
    timestamp: datetime
    source: str

    def to_json_str(self):
        return dumps(self.__dict__, default=lambda x: x.__dict__, indent=2)

    