import random
from langchain.chat_models import GigaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from gigachat.models import Chat, Messages, MessagesRole

# Авторизация в сервисе GigaChat
andyCred = "MTI3YzYzN2ItOGIwOC00NDNiLWJmOGItOGM3N2NmNTYxMjZhOjVjYWYxMjljLWJlMjEtNDQ4Yi05M2Q5LTI1N2ZhMmEzMmU2Mw=="
keyWorlds = [["Python","0"],["Java","1"],["PHP","2"],["C++","3"]]

'''
chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False)

messages = [
    SystemMessage(
        # role = MessagesRole.USER,
        role = MessagesRole.ASSISTANT,
        # temperature = 2,
        # content="придумать сложный вопрос по Python с примером"
        # content="Напиши 3 вопроса для senior Python"
        # content="Ты рекрутер по senior Python. Напиши 3 вопроса"
        # content="Напиши 5 вопросов по Python"
        # content="Ты рекрутер Напиши 3 вопроса"
        content="Составить вопросы senior-java"
    )
]
res = chatAndy(messages)
messages.append(res)
print(res.content)
'''
class gigaChatProcessor:
    def __init__(self):
        self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False)
        self.counter = 0
        return
    def testKey(self, testedUserWorks):
        keyAdded = []
        for key in keyWorlds:
            if key[0].lower() in testedUserWorks.lower():
                keyAdded.append(key)
                
        return keyAdded
    def start(self, keyAdded):
        lenKey = len(keyAdded)
        indexKey = random.randint(0,lenKey-1)
        roleReq = MessagesRole.ASSISTANT
        prefReq =""
        self.counter = 1
        if self.counter == 0:
            roleReq = MessagesRole.SYSTEM
            msgReq = "Ты рекрутер. начальный  вопрос кандидату"
            indexKey = -1
            prefReq = "[общ.] "
        else:
            msg = keyAdded[indexKey]
            prefReq = f"[{msg[0]}] "
            # msgReq = f"Напише мне вопрос по {msg[0]} кандидату на должность ведущего программиста"
            msgReq = f"Ты рекрутер. Напише мне задачу на {msg[0]} для кандидата на должность ведущего программиста"
        messages = [
            SystemMessage(
                # role = MessagesRole.USER,
                role = roleReq,
                # temperature = 2,
                content=msgReq
            )
        ]
        res =self.chatAndy(messages)
        messages.append(res)
        self.counter += 1
        outStr = res.content
        indexStart = outStr.find(":")
        if indexStart > 0:
            outStr = outStr[indexStart+3:]
        return prefReq + res.content


        
