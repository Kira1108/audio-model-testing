import logging
logging.basicConfig(level = logging.INFO)
from funasr import AutoModel
from functools import lru_cache
from timer import timer

@lru_cache(maxsize = None)
def load_model(model: str = "ct-punc"):
    return AutoModel(model=model)

class PuncCreator:
    """Add punctuations to Chinese text with FunASR models."""
    def __init__(self, model: str = "ct-punc"):
        self.model = load_model(model)
        
    @timer(name = "Punctuation generation")
    def create_punc(self, text: str):
        return self.model.generate(input=text)[0]['text']
    
    def __call__(self, text: str):
        return self.create_punc(text)
    

if __name__ == "__main__":
    punc = PuncCreator()
    result_str = punc.create_punc("团队是个人的延伸 胖子哥 你说对不对")
    print(result_str)