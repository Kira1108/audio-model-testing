from ollama import chat
from ollama import ChatResponse
import time
# 这个问题真难，草

DUPLEX_PROMPT = """
角色： 双工客服代理。                                                                    

任务： 您将收到实时转换的客户服务ASR文本。文本可能不完整。                                   
您应该输出一个信号，无论是开始回应用户还是继续倾听，直到理解用户的查询。                     
请注意，用户是通过电话说话，之前的步骤对音频片段的含义一无所知，因此文本可能不完整。 
不要管用户的问题中涵盖的业务，仅从文本本身判断，用户是否说完了，以及客服是不是可以开始回答。        

信号输出：                                                                                   
 1 如果文本完整且问题组成部分清晰，您应该输出'reply'，表示现在是回应用户的正确时间。         
 2 如果文本不完整或问题组成部分不清晰，您应该输出'wait'，表示现在不是回应用户的正确时间，需要
   继续倾听。                                                                                
 3 特殊情况：如果问题本身不完整以至于无法回答，但用户似乎在等待回应，您应该输出'followup'，表
   示您应该请求更多信息或简单地与用户交谈。                                                  
   在后续情况下，您应该像真正的人类客服人员一样有礼貌。                                      

预期输出格式是有效的Json代码块，用三个反引号(json...)括起来。 json对象的键如下： 
{{ "signal": // str, 从三种状态中选一个：'reply', 'wait', 'followup'。
"following_up_question": // str, 如果signal是'followup'，提出一个跟进的问题，或者与用户聊天 }}                                      
现在用户输入是：我想了解一下你们的贷款产品，003号产品，我可以申请么。 
输出 =
"""


start = time.time()
response: ChatResponse = chat(model='tulu3', messages=[
  {
    'role': 'user',
    'content': DUPLEX_PROMPT,
  },
])

print(response.message.content)
print(f"Taking {time.time() - start} seconds")

