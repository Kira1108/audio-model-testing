from functools import lru_cache
from funasr import AutoModel
from dataclasses import dataclass
from timer import timer
from typing import Union
import numpy as np

@lru_cache(maxsize = None)
def load_model():
   return AutoModel(model="fsmn-vad")


@dataclass
class Vad:
    def __post_init__(self):
        self.model = load_model()
        self.cache = {}
        self.chunk_size = 200
    
    @timer("VAD")  
    def vad(self, speech_chunk:Union[np.array, list],is_final:bool = False):
        return self.model.generate(
            input=speech_chunk, cache=self.cache, is_final=is_final, chunk_size=self.chunk_size)[0]['value']
    
def test_paraformer():
    import soundfile
    import os
    from punctuations import PuncCreator
    punc = PuncCreator()
    chunk_stride = 9600
    vad = Vad()
    fp = "datafiles/asr_example.wav"
    speech, sample_rate = soundfile.read(fp)
    total_chunk_num = int(len((speech)-1)/chunk_stride+1)

    for i in range(total_chunk_num):
        res = vad.vad(
            speech[i*chunk_stride:(i+1)*chunk_stride], 
            i == total_chunk_num - 1
        )
        print(res)
        
if __name__ == "__main__":
    test_paraformer()

