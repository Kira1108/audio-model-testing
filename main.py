from recordings import AudioRecorder
from whisper import WhisperASR

agen = AudioRecorder()
whisper = WhisperASR()

samples = []
for chunk in agen.gen_chunks(10):
    samples.extend(chunk)
    
print(whisper(samples, 16000))
    
    