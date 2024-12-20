import soundfile
import os
from punctuations import PuncCreator
from paraformer import Paraformer
from vad import Vad
from audio_loader import load_file

def streaming_audio(fp = "datafiles/asr_example.wav"):
    """手动撕开音频文件测试流式处理流程"""
    
    # 添加标点符号
    punc = PuncCreator()
    
    # 语音断点检测
    vad = Vad()
    chunk_stride = 9600
    
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

    def asr(self, speech_chunk, is_final=False):
        # Perform ASR on the speech chunk
        res = self.paraformer.stream_asr(speech_chunk, is_final)
        self.buffer += res
        
        # Check for speech breakpoints using VAD
        if self.vad.shutup(speech_chunk, is_final) and len(self.buffer) > 0:
            # Add punctuation to the buffer
            display = self.punc.create_punc(self.buffer)
            self.buffer = ""  # Clear the buffer after punctuation is added
            yield display




if __name__ == "__main__":
    streaming_audio("datafiles/output.wav")