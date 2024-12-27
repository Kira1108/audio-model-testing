from ollama import chat
from ollama import ChatResponse
import time
import copy
from timer import timer


def car_RAG_bot(query:str) -> int:
    """Use advanced RAG technology to get knowledge from Mivuls vector db and answer user quest
    Is is suggested all car related questions are asked to this bot
    Args:
        query:str: the user query
        
    Returns:
        str: answer to the user query
    """
    
    return "特斯拉Model Y在北京的价格是500000人民币"

DUPLEX_PROMPT = """
You are a helpful customer service assistant in the automobile industry. You answer user questions and chat with users via telephone.
Assist the user and help them with their problems.

The user query is sent via streamed voice input (converted with ASR). Therefore, the current chunk of text may not be the end of the user query.
A complete query is semantically complete. Do not worry about the business logic of the query; just judge literally whether it is complete or not.

If the current query is complete and it is an appropriate time to answer, you reply to the user.
If the current query is incomplete, you should output a signal <idle> to indicate that you are still waiting for the user to finish speaking.

If in any case the user query is incomplete, wait carefully util the user finishes speaking(judged semantically).

The conversation make take several turns, in each turn, the user query may be complete or incomplete. 

Examples:

1. User: "Can you tell me the price of the new model?"
   Assistant: "The price of the new model is $25,000."

2. User: "I need to book a service appointment for my" # Incomplete query
   Assistant: <idle>

3. User: "What are the available colors for the latest SUV?"
   Assistant: "The available colors for the latest SUV are red, blue, black, and white."

4. User: "How long does it take to" # Incomplete query， you should wait
   Assistant: <idle>

5. User: "Can you help me with the warranty details?"
   Assistant: "Sure, the warranty covers 3 years or 36,000 miles, whichever comes first."
   
6. AI:Hello there, how can I help you today?
   User: 你好。# greeting in Chinese
   AI:您好，有什么可以帮助您的吗？ # reply greeting in Chinese
   User: 请问，你 # incomplete query
   AI:<idle> # wait for user to finish speaking
   User: 门公司有没有贷款产  # incomplete query
   AI:<idle> # wait for user to finish speaking
   User: 品 # complete query
   AI:我们公司提供贷款服务, 比如有.... # reply to user query in Chinese
   
Note: continuous empty user query input may be a signal that the user has finished speaking. You should responde immediately in this case.
   
BE SURE TO USE TOOL TO ANSWER ALL USER QUERY RELATED TO CAR PARAMETERS, PRICES, AUTOMOBILE LOAN and CAR INSURANCE.
Make sure to reply less than 100 Chinese characters in each response.
If you gonna reply the user, please use the same language as the user.
"""


def start_chat_duplex():
    
    messages = messages=[
        {
            'role': 'system',
            'content': DUPLEX_PROMPT,
        }
    ]
    print("Hello there, how can I help you today?")
    
    while True:
        user_query = input("User: ")
        
        messages.append({
            'role': 'user',
            'content': user_query,
        })
        start = time.time()
        response: ChatResponse = chat(model='qwen2.5:14b', messages=messages,
                                      tools=[car_RAG_bot])
        
        print(response.message.tool_calls)
        end = time.time()
        print("Time taken: ", end-start)
        
        # 此处只有TTS在双工对话中播放了这个语音，它才应该加入到message中
        messages.append({
            'role': 'assistant',
            'content': response.message.content,
        })
        print("AI: ",response.message.content)


class DuplexChatter:
   
    def __init__(self, 
                 sys_prompt:str = None, 
                 knowledge:str = None):
        
        if not sys_prompt:
            sys_prompt = "You are a helpful assitant."
            
        if knowledge:
            sys_prompt += f"{sys_prompt}\nWhen necessary, refer to the following knowledge to provide useful information: \n<knowledge>{knowledge}</knowledge>"
            
        self.messages = [
            {'role': 'system','content': sys_prompt}
        ]
        
    @classmethod
    def demo(cls):
        return cls(
            sys_prompt = DUPLEX_PROMPT, 
            knowledge = "Car related information:我们公司特斯拉Model Y在北京的价格是500000人民币， 在天津的价格是480000人民币")
        
    @property
    def history(self) -> str:
        return '\n'.join([f"{m['role']}: {m['content']}" for m in self.messages])
        
    def add_user_query(self, query:str):
        self.messages.append({
            'role': 'user',
            'content': query,
        })
        
    def add_assistant_reply(self, reply:str):
        self.messages.append({
            'role': 'assistant',
            'content': reply,
        })
        
    @timer("Qwen Model")
    def chat(self, query:str):
        messages = copy.deepcopy(self.messages)
        messages.append({
            'role': 'user',
            'content': query}
        )
        response: ChatResponse = chat(model='qwen2.5:14b', messages=messages)
        return response.message.content

if __name__ == "__main__":
    start_chat_duplex()
