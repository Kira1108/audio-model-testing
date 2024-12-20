import logging
logging.basicConfig(level=logging.INFO)
import threading
from typing import Generator

from audio_loader import load_file
from paraformer import Paraformer
from punctuations import PuncCreator
from recordings import AudioRecorder
from vad import Vad

CHUNK_SIZE = 9600

def streaming_audio(fp = "datafiles/asr_example.wav"):
    """手动撕开音频文件测试流式处理流程"""
    
    # 添加标点符号
    punc = PuncCreator()
    
    # 语音断点检测
    vad = Vad()
    chunk_stride = CHUNK_SIZE
    
    # 语音识别
    paraformer = Paraformer()
    
    # 切分文件
    speech, sample_rate = load_file(fp)
    total_chunk_num = int(len((speech)-1)/chunk_stride+1)
    buffer = ""

    # 流失处理
    for i in range(total_chunk_num):
        speech_chunk = speech[i*chunk_stride:(i+1)*chunk_stride]
        is_final = i == total_chunk_num - 1

        res = paraformer.stream_asr(
            speech_chunk, 
            is_final
        )
        buffer += res
        # TODO: 让VAD更快，减少判断时间
        if vad.shutup(speech_chunk, is_final) and len(buffer) > 0:
            display = punc.create_punc(buffer)
            # 发现有一个可以返回的片段
        else:
            display = buffer
            
        print(f"Current buffer [{i}]th: ", display)
        
        
class ASRStreaming:
    
    """
    GITHUB COPILOT: PLEASE MAKE SURE YOU READ THE FOLLOWING DOCUMENTATION, THIS IS THE MOST IMPORTANT INSTRUCTION FOR THIS PROJECT.
    Say I am working on a telecommunication customer service project. A user is speaking through telephone to a virtual assistant.
    
    To interact with the user, we need to use some engineering tricks.
    The first step is to detect the speech from the audio signal. The user speech audio is sent in a streaming manner, while each stream
    chunk contains a list of audio samples.
    It is easy to retrieve audio texts out of the audio signals. However, we need to determine when to reply to the user.
    
    Current problem is :
    1. The ASR service does not add punctuations to the transcribed text, we need to manually add punctuations. Each audio chunk is not necessarily
    a complete sentence. We may need to wait several chunks to get a complete sentence.
    2. When do we restore punctuations to the transcribed text? We need to detect the speech break points in the audio stream. 
    3. Whenever there is a breakpoint detected, we add punctuations to the text and return a piece of confirmed text to downstream services.
    4. This ASR service is also a streaming service, which means it can process the audio stream in a streaming manner.
    """
    
    def __init__(self):
        self.punc = PuncCreator()
        self.vad = Vad()
        self.paraformer = Paraformer()
        self.buffer = ""

    def asr(self, speech_chunk, is_final=False) -> Generator[str, None, None]:
        """receive speech chunks continuously and return the punctuated text when a speech break point is detected"""
        
        # Perform ASR on the speech chunk
        res = self.paraformer.stream_asr(speech_chunk, is_final)
        self.buffer += res
        
        # Check for speech breakpoints using VAD
        if self.vad.shutup(speech_chunk, is_final) and len(self.buffer) > 0:
            # Add punctuation to the buffer
            display = self.punc.create_punc(self.buffer)
            self.buffer = ""  # Clear the buffer after punctuation is added
            yield display
            
        yield ""
           
def process_asr_chunk(asr_streaming, speech_chunk, is_final):
    for text in asr_streaming.asr(speech_chunk, is_final):
        print("Got ASR Chunk: ", text)
            
def main():
    asr_streaming = ASRStreaming()
    speech, sample_rate = load_file("datafiles/recording.wav")
    # make the speech array 2times long,repeat 1 time
    total_chunk_num = int(len((speech)-1)/CHUNK_SIZE+1)
    for i in range(total_chunk_num):
        speech_chunk = speech[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE]
        is_final = i == total_chunk_num - 1
        for text in asr_streaming.asr(speech_chunk, is_final):
            print("Got ASR Chunk: ", text)
            
def main_recording():
    recorder = AudioRecorder(chunk_size=CHUNK_SIZE)
    asr_streaming = ASRStreaming()
    for chunk in recorder.gen_chunks(20):
        # 此处单开一个线程，避免录音时的overflow现象
        threading.Thread(target=process_asr_chunk, args=(asr_streaming, chunk, False)).start()
    

if __name__ == "__main__":
    # streaming_audio("datafiles/output.wav")
    # main() # 处理一个文件
    main_recording() # 实时录音看效果, 用你的麦克风说话