# Note on audio processing

## 1. Packages and installations
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

## 2. Parameters and concepts


**Rate**    
The RATE parameter in the context of audio recording and playback refers to the sample rate, which is the number of samples of audio carried per second. It is measured in Hertz (Hz).

In your code, RATE is set to 44100, which means the audio is sampled 44,100 times per second. This is a common sample rate for high-quality audio and is the standard for CD audio.

Here's a brief explanation of why sample rate is important:

Higher sample rates can capture more detail in the audio signal, leading to higher fidelity recordings.
Lower sample rates reduce the amount of data and can be sufficient for applications where high fidelity is not necessary, such as voice recordings.
In summary, RATE = 44100 means that the audio will be recorded at a sample rate of 44,100 samples per second, ensuring high-quality audio capture.

> 音频文件每秒的信号数量。


The total number of audio samples (signal points) recorded will be the sample rate (RATE) multiplied by the duration of the recording (RECORD_SECONDS).

Given: RATE = 44100 samples per second     
RECORD_SECONDS = 5 seconds     
The total number of signal points will be:    
$[ 44100 , \text{samples/second} \times 5 , \text{seconds} = 220500 , \text{samples} ]$


So, the final number of signal points recorded will be 220,500.

---
**Chunk**    
In the context of audio processing, the CHUNK parameter defines the number of frames (samples) that are read from the audio input stream at a time. It essentially determines the size of the buffer used for reading and writing audio data.

Here's a breakdown of its role:

Buffer Size: CHUNK specifies the size of the buffer in frames. In your code, CHUNK is set to 1024, meaning that 1024 frames are processed in each read/write operation.
Latency: A smaller CHUNK size can reduce latency, making the audio processing more responsive. However, it may increase the CPU load due to more frequent read/write operations.
Efficiency: A larger CHUNK size can be more efficient in terms of CPU usage, as it reduces the number of read/write operations. However, it can increase latency.
In your code, the CHUNK size is used in the loop that reads audio data from the input stream and writes it to the output file:

This loop reads CHUNK frames at a time from the audio input stream and writes them to the output file, repeating until the total recording duration is reached.

In summary, CHUNK = 1024 means that audio data is processed in chunks of 1024 frames at a time.


The expression RATE // CHUNK * RECORD_SECONDS calculates the total number of chunks that will be processed during the recording period.

Here's the step-by-step breakdown:

RATE // CHUNK: This calculates how many chunks fit into one second of audio. Given RATE = 44100 samples per second and CHUNK = 1024 samples per chunk: $[ \text{Chunks per second} = \frac{44100}{1024} \approx 43 ]$

RATE // CHUNK * RECORD_SECONDS: This calculates the total number of chunks for the entire recording duration. Given RECORD_SECONDS = 5 seconds: $[ \text{Total chunks} = 43 \times 5 = 215 ]$

So, the loop will iterate 215 times, reading and writing 1024 samples (one chunk) each time, to cover the entire 5-second recording period.

---
**Streaming**     
The stream object in PyAudio functions similarly to a Python generator, providing a continuous flow of audio data in chunks of the specified size. Here's a more detailed explanation:

Opening the Stream: The stream object is created using the p.open() method, which sets up the audio input stream with the specified format, channels, and rate.

FORMA
Reading Data in Chunks: The stream.read(CHUNK) method reads the next CHUNK size of audio data from the input stream. Each call to stream.read(CHUNK) returns the next 1024 samples (in this case) of audio data.

Stateless Operation: The stream object does not maintain state about the previously read data. Each call to stream.read(CHUNK) is independent and only returns the current chunk of audio data. This is similar to how a generator yields the next value in a sequence without retaining information about previous values.

Writing Data: The read data is then written to the output file using wf.writeframes(). This process continues until the total number of chunks for the recording duration is processed.

In summary, the stream object acts like a valve, providing a continuous flow of audio data in chunks. It does not retain information about previously provided data, focusing only on the current chunk being read.


