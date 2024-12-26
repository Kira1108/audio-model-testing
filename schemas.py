from dataclasses import dataclass
import numpy as np

@dataclass
class AudioChunk:
    """
    Desc: Audio chunk dataclass
    Args:
        chunk_id: chunk id, starts from 0, increment by 1, sequentially.
        relative_ts: relative timestamp, in seconds, representing the ending time point of the chunk.
        data: audio data as numpy array
    """
    
    chunk_id:int
    relative_ts:float
    data:np.array
    
    def to_dict(self):
        return {
            "chunk_id": self.chunk_id,
            "relative_ts": self.relative_ts,
            "data": self.data.tolist()
        }
        
@dataclass
class TextChunk:
    """
    Desc: Text chunk dataclass
    Args:
        chunk_id: int, starts from 0, increment by 1, sequentially.
        max_relative_ts: float, maximum relative timestamp of the chunk, in seconds
        text: str, asr transcribed text.
        
    Note: a text chunk is a piece of text that is transcribed from multiple audio chunks.
    Text chunk is associated with a maximum relative timestamp, which is the ending time point of the last audio chunk.
    """
    
    chunk_id:int
    max_relative_ts:float
    text:str