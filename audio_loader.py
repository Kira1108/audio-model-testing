import librosa

def load_file(fp):
    audio, sampling_rate = librosa.load(fp, sr=None)
            
    if sampling_rate != 16000:
        audio = librosa.resample(audio, orig_sr=sampling_rate, target_sr=16000)
        sampling_rate = 16000
        
    return audio, sampling_rate