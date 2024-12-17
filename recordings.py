import sys
import pyaudio
import struct
import numpy as np
from dataclasses import dataclass
from typing import Any
import wave

@dataclass
class AudioRecorder:
    """
    Desc: Record audio from microphone
    Args:
        chunk_size: number of samples per chunk
        audio_format: pyaudio audio format
        channels: number of channels
        rate: sampling rate, we use 16000 Hz which is required by Whisper model
        
    Methods:
        gen_chunks: generate audio chunks from microphone, this generator returns audio samples as list
    """
    
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
        
    def record_and_save(self, seconds = 10):
        samples = []
        for chunk in self.gen_chunks(seconds):
            samples.extend(chunk)
        
        with wave.open("datafiles/recording.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes((np.array(samples) * 32768.0).astype(np.int16).tobytes())
        print("Recording saved as output.wav")
        
if __name__ == "__main__":
    agen = AudioRecorder()
    agen.record_and_save(3)
    samples = []
    for chunk in agen.gen_chunks(5):
        print(chunk[:20])
        samples.extend(chunk)
    print("Total samples:", len(samples))
    
    

