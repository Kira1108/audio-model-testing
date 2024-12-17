import sys
import pyaudio
import struct
import numpy as np
from dataclasses import dataclass
from typing import Any

@dataclass
class AudioRecorder:
    chunk_size:int = 1024
    audio_format:Any = pyaudio.paInt16
    channels:int = None
    rate:int = 16000
    
    def __post_init__(self):   
        if self.channels is None:
            self.channels = 1 if sys.platform == 'darwin' else 2
        self.p = pyaudio.PyAudio()
        
    def gen_chunks(self, seconds:int = 10):
        stream = self.p.open(
            format=self.audio_format, 
            channels=self.channels, 
            rate=self.rate, 
            input=True)
        
        print('Recording...')
        for _ in range(0, self.rate // self.chunk_size * seconds):
            chunk = stream.read(self.chunk_size)
            fmt = f"{len(chunk) // 2}h"
            samples = struct.unpack(fmt, chunk)
            samples = np.array(samples, dtype = np.int16)
            if self.channels == 2:
                samples = samples.reshape(-1, 2)
                samples = samples.mean(axis=1).astype(np.int16)
            samples = samples / 32768.0
            yield samples.tolist()
        print('Recording Done...')
        stream.close()
        self.p.terminate()
        
if __name__ == "__main__":
    agen = AudioRecorder()
    samples = []
    for chunk in agen.gen_chunks(5):
        print(chunk[:20])
        samples.extend(chunk)
    print("Total samples:", len(samples))
    
    

