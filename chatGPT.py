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
    def start(self):
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
                # content="Составить вопросы senior-java"
                content="что такое def в python"
            )
        ]
        res =self.chatAndy(messages)
        messages.append(res)
        self.counter += 1
        return res.content 


        
