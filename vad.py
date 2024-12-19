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
        
    def shutup(self, speech_chunk:Union[np.array, list], is_final:bool = False):
        """
        Note: The output format for the streaming VAD model can be one of four scenarios:

        [[beg1, end1], [beg2, end2], .., [begN, endN]]：The same as the offline VAD output result mentioned above.
        
        [[beg, -1]]：Indicates that only a starting point has been detected.
        [[-1, end]]：Indicates that only an ending point has been detected.
        []：Indicates that neither a starting point nor an ending point has been detected.
        """
        intervals = self.vad(speech_chunk, is_final)
        
        if not len(intervals) > 0:
            return False
        
        last = intervals[-1]
        
        if len(last) > 0 and last[-1] >0:
            return True
        
        return False
    
def test_vad():
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
    test_vad()

