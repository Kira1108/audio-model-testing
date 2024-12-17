from recordings import AudioRecorder
from whisper import WhisperASR

sampling_rate = 16000
agen = AudioRecorder()
whisper = WhisperASR()

samples = []
for chunk in agen.gen_chunks(seconds = 5):
    samples.extend(chunk)
    # print(whisper(chunk, sampling_rate))
    
print(whisper(samples, sampling_rate))