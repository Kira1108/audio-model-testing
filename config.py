import torch
from dataclasses import dataclass
from functools import lru_cache

@dataclass
class Config:
    device:str = None
    
    def __post_init__(self):
        if not self.device:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            # self.device = "cuda" if torch.cuda.is_available() else \
            #     "mps" if torch.backends.mps.is_available() else \
            #     "cpu"
                
                
@lru_cache(maxsize = None)
def get_config():
    return Config()