import logging
logging.basicConfig(level = logging.INFO)
from dataclasses import dataclass, field
from functools import lru_cache
from funasr import AutoModel
from typing import Union
import numpy as np
from timer import timer


@lru_cache
def load_model():
    return AutoModel(model="paraformer-zh-streaming")

@dataclass
class Paraformer:
    chunk_size: list = field(default_factory=lambda: [0, 10, 5])
    encoder_chunk_look_back: int = 4
    decoder_chunk_look_back: int = 1
    
    def __post_init__(self):
        self.model = load_model()
        self.cache = {}
    
    def step(self, speech_chunk:Union[list, np.array], is_final:bool = False):
        if isinstance(speech_chunk, list):
            speech_chunk = np.array(speech_chunk)
            
        return self.model.generate(
            input=speech_chunk, 
            cache=self.cache, 
            is_final=is_final, 
            chunk_size=self.chunk_size, 
            encoder_chunk_look_back=self.encoder_chunk_look_back, 
            decoder_chunk_look_back=self.decoder_chunk_look_back
        )
        
    @timer(name = "ParaformerStreaming")
    def stream_asr(self, 
                   speech_chunk:Union[list, np.array], 
                   is_final:bool = False):
        if isinstance(speech_chunk, list):
            speech_chunk = np.array(speech_chunk)
            
        return self.step(speech_chunk, is_final)[0]['text']
        
        
def test_paraformer():
    import soundfile
    import os
    from punctuations import PuncCreator
    punc = PuncCreator()
    chunk_stride = 9600
    paraformer = Paraformer()
    fp = "datafiles/asr_example.wav"
    speech, sample_rate = soundfile.read(fp)
    total_chunk_num = int(len((speech)-1)/chunk_stride+1)
    buffer = ""

    for i in range(total_chunk_num):
        res = paraformer.stream_asr(
            speech[i*chunk_stride:(i+1)*chunk_stride], 
            i == total_chunk_num - 1
        )
        buffer += res
        display = buffer if len(buffer) == 0 else punc.create_punc(buffer)
        print(f"Current buffer [{i}]th: ", display)
        
if __name__ == "__main__":
    test_paraformer()