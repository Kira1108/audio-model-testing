import logging
logging.basicConfig(level = logging.INFO)
from funasr import AutoModel
from functools import lru_cache
from timer import timer
# TODO: 换成流式的标点还原
# https://github.com/modelscope/FunASR/blob/main/examples/industrial_data_pretraining/ct_transformer_streaming/demo.py

@lru_cache(maxsize = None)
def load_punc_model(model: str = "ct-punc"):
    return AutoModel(model=model)

class PuncCreator:
    """Add punctuations to Chinese text with FunASR models."""
    def __init__(self, model: str = "ct-punc"):
        self.model = load_punc_model(model)
        
    @timer(name = "Punctuation generation")
    def create_punc(self, text: str):
        return self.model.generate(input=text)[0]['text']
    
    def __call__(self, text: str):
        return self.create_punc(text)
    

if __name__ == "__main__":
    punc = PuncCreator()
    result_str = punc.create_punc("说你呢看啥呢脑子有问题吧擦")
    print(result_str)