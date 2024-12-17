from funasr import AutoModel
from functools import lru_cache

@lru_cache(maxsize = None)
def load_model(model: str = "ct-punc"):
    return AutoModel(model=model)

class PuncCreator:
    """Add punctuations to Chinese text with FunASR models."""
    def __init__(self, model: str = "ct-punc"):
        self.model = load_model(model)
        
    def create_punc(self, text: str):
        return self.model.generate(input=text)[0]['text']
    
    def __call__(self, text: str):
        return self.create_punc(text)
    

if __name__ == "__main__":
    punc = PuncCreator()
    result_str = punc.create_punc("那今天的会就到这里吧 happy new year 明年见")
    print(result_str)