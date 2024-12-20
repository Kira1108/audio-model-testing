import logging
from functools import lru_cache
from typing import List

from funasr import AutoModel

from timer import timer

# TODO: 换成流式的标点还原
# https://github.com/modelscope/FunASR/blob/main/examples/industrial_data_pretraining/ct_transformer_streaming/demo.py

@lru_cache(maxsize = None)
def load_punc_model(stream = False):
    if not stream:
        return AutoModel(model="ct-punc")
    return AutoModel(model="iic/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727")

class PuncCreator:
    """Add punctuations to Chinese text with FunASR models."""
    def __init__(self):
        self.model = load_punc_model(stream = False)
        
    @timer(name = "Punctuation generation")
    def create_punc(self, text: str):
        return self.model.generate(input=text)[0]['text']
    
    def __call__(self, text: str):
        return self.create_punc(text)
    
    
class StreamPuncCreator:
    """Add punctuations to Chinese text with FunASR models."""
    def __init__(self):
        self.model = load_punc_model(stream = True)
        self.cache = {}
        
    @timer(name = "Stream Punctuation generation")
    def create_punc(self, text: str):
        return self.model.generate(input=text, cache = self.cache)[0]['text']
    
    def __call__(self, text: str):
        return self.create_punc(text)
    
    

if __name__ == "__main__":
    punc = PuncCreator()
    result_str = punc.create_punc("说你呢看啥呢脑子有问题吧擦")
    print(result_str)