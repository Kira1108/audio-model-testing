import logging
logging.basicConfig(level = logging.INFO)
from funasr import AutoModel
from functools import lru_cache
from timer import timer
from typing import List

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
    
    
# from funasr import AutoModel

# model = AutoModel(model="iic/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727")

# inputs = "欢迎体验这个|阿里巴巴|这个达摩院的|大模型|总的来说|这个大模型还是不错的|真的很好了|希望大家喜欢|我说完了|哈哈|"
# vads = inputs.split("|")
# rec_result_all = "outputs: "
# cache = {}
# for vad in vads:
#     rec_result = model.generate(input=vad, cache=cache)
#     rec_result_all += rec_result[0]["text"]
# print(rec_result_all)
    

if __name__ == "__main__":
    punc = PuncCreator()
    result_str = punc.create_punc("说你呢看啥呢脑子有问题吧擦")
    print(result_str)