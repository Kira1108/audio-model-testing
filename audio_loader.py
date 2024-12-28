import librosa
import time
from typing import Generator, Union
import numpy as np
import math
import soundfile as sf

def load_file(fp):
    """
    Load an audio file and resample it to 16000 Hz if necessary.
    Parameters:
    fp (str): File path to the audio file.
    Returns:
    tuple: A tuple containing:
        - audio (numpy.ndarray): The audio time series.
        - sampling_rate (int): The sampling rate of the audio time series.
    """
    audio, sampling_rate = librosa.load(fp, sr=None)
            
    if sampling_rate != 16000:
        audio = librosa.resample(audio, orig_sr=sampling_rate, target_sr=16000)
        sampling_rate = 16000
    return audio, sampling_rate

def audio_gen_stream(
    audio: Union[np.ndarray, list],
    chunk_size: int = 1024, 
    sr: int = 16000
) -> Generator[np.ndarray, None, None]:
    """
    Generates audio chunks from a given audio array or list.
    Args:
        audio (Union[np.ndarray, list]): The input audio data, either as a NumPy array or a list.
        chunk_size (int, optional): The size of each audio chunk in samples. Defaults to 1024.
        sr (int, optional): The sample rate of the audio data. Defaults to 16000.
    Yields:
        Generator[np.ndarray, None, None]: A generator that yields audio chunks as NumPy arrays.
    """
    
    if isinstance(audio, list):
        audio = np.array(audio)
    
    chunk_during = chunk_size / sr
    n_chunks = math.ceil(len(audio) / chunk_size)
    for i in range(n_chunks):
        time.sleep(chunk_during)
        chunk = audio[i*chunk_size:(i+1)*chunk_size]
        yield chunk
        
def audio_gen_file(
    fp: str, 
    chunk_size: int = 1024, 
    sr: int = 16000, 
    force_sr_normalize: bool = True
    ) -> Generator[np.ndarray, None, None]:
    """
    Generates audio data from a file in chunks.
    Parameters:
        fp (str): File path to the audio file.
        chunk_size (int, optional): Size of each chunk to be generated. Default is 1024.
        sr (int, optional): Sample rate for the audio file. Default is 16000.
        force_sr_normalize (bool, optional): If True, resample the audio to 16000 Hz if it is not already. Default is True.
    Returns:
        Generator[np.ndarray, None, None]: A generator that yields chunks of audio data as numpy arrays.
    """
    
    audio, sr = sf.read(fp)
    if force_sr_normalize and (not sr == 16000):
        audio = librosa.resample(audio, sr, 16000)
    return audio_gen_stream(audio, chunk_size=chunk_size, sr=sr)