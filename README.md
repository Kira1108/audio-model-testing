# Note on audio processing

1. Install librosa and soundfile to handle audio files.
2. Install pyaudio to perform real-time audio processing.[pyAudio documentation](!https://people.csail.mit.edu/hubert/pyaudio/), follow the instruction to install pyaudio.

On macOS, we use the following method to install
```bash
brew install portaudio
pip install pyaudio
```
3. Download asr model: there are many version of openai Whisper model on huggingface, we choose the tiny one for macOS testing purpose.

4. We may need to install additional libraries such as `ffmpeg`, `libsndfile`, and `portaudio` to handle audio files and real-time audio processing. On macOS, we can use homebrew to install these libraries.
```bash
brew install ffmpeg
brew install libsndfile
brew install portaudio
```

> We may need to create a Docker container to run audio related code, such that the environment is independent of the host machine.


pyaudio full duplex wire mode is useful in real-time audio processing.
```python
"""PyAudio Example: full-duplex wire between input and output."""

import sys
import pyaudio

RECORD_SECONDS = 5
CHUNK = 1024
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),
                channels=1 if sys.platform == 'darwin' else 2,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print('* recording')
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    stream.write(stream.read(CHUNK))
print('* done')

stream.close()
p.terminate()
```