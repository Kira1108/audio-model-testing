import soundfile
import os
from punctuations import PuncCreator
from paraformer import Paraformer
from vad import Vad

def streaming_audio(fp = "datafiles/asr_example.wav"):
    punc = PuncCreator()
    vad = Vad()
    chunk_stride = 9600
    paraformer = Paraformer()
    speech, sample_rate = soundfile.read(fp)
    total_chunk_num = int(len((speech)-1)/chunk_stride+1)
    buffer = ""

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
            # 判断标点是否结束标点
            # 如果是结束标点，llm(buffer) -> tts(buffer)
        else:
            display = buffer
            
        print(f"Current buffer [{i}]th: ", display)
        
if __name__ == "__main__":
    streaming_audio()