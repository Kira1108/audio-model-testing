import logging
logging.basicConfig(level = logging.INFO)
from transformers import (
    WhisperProcessor, 
    WhisperForConditionalGeneration
)
import torch
import logging
from dataclasses import dataclass
from functools import lru_cache
import time

def time_tracker(name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            total_time = end_time - start_time
            logging.info(f"{name} - Total time cost: {total_time:.4f} seconds")
            return result
        return wrapper
    return decorator

@lru_cache(maxsize = None)
def load_asr_model(device:str = None):
    logging.info("Loading Whisper model and processor")
    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
    model.config.forced_decoder_ids = None

    if device is None:
        device = "cuda" if torch.cuda.is_available() \
            else "mps" if torch.backends.mps.is_available() \
            else "cpu"
        
    device = torch.device(device)
    model.to(device)
    logging.info(f"Whisper model is running on {str(device)}")
    return  model, processor, device

@dataclass
class WhisperASR:
    
    device:str = None
    
    def __post_init__(self):
        self.model, self.processor, self.device = load_asr_model(self.device)
        
    def transcript_file(self, fp:str):
        try:
            import librosa
        except:
            raise ImportError("librosa is required for file processing")
        
        audio, sampling_rate = librosa.load(fp, sr=None)
        
        if sampling_rate != 16000:
            audio = librosa.resample(audio, orig_sr=sampling_rate, target_sr=16000)
            sampling_rate = 16000
            
        return self.transcript(audio, sampling_rate)
        
    def create_features(self, signal, sampling_rate):
        "Converting audio signal to huggingface input features"
        return self.processor(
            signal, 
            sampling_rate=sampling_rate, 
            return_tensors="pt").input_features.to(self.device)
    
    def generate(self, input_features):
        "Generate text tokens from input features"
        return self.model.generate(input_features)
    
    def decode(self, predicted_ids):
        "Decode token ids to text"
        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
    
    @time_tracker("ASR")
    def transcript(self, signal, sampling_rate):
        "Generate transcription from audio signal"
        input_features = self.create_features(signal, sampling_rate)
        predicted_ids = self.generate(input_features)
        transcription = self.decode(predicted_ids)
        return transcription
    
    def __call__(self, signal, sampling_rate):
        "Generate transcription from audio signal"
        return self.transcript(signal, sampling_rate)

if __name__ == "__main__":
    asr = WhisperASR(device="mps")
    fp = "/Users/mac/projects/audio-model-testing/datafiles/output.wav"
    transcription = asr.transcript_file(fp)
    print(transcription)


