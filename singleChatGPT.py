import random
from langchain.chat_models import GigaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.prompts import load_prompt
from langchain.chains import LLMChain

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from gigachat.models import Chat, Messages, MessagesRole


class singleChat:
    def __init__(self, gigaChat) -> None:
        self.chatAndy = gigaChat
        self.counter = 0
        self.messages = None

    def gptRequst(self, roleReuest, requestMsg):
        self.messages = [
            SystemMessage(
                role = roleReuest,
                content=requestMsg
            )
        ]
        res =self.chatAndy(self.messages)
        self.messages.append(res)
        self.counter += 1
        return res.content         

    # def doFullGptRequst(self, key):
        
    #     role = MessagesRole.ASSISTANT
    #     text ="Придумай соискателю сложную вопрос по OpenGL. Я опытный программист"
        
    #     inf0 = singleChat.gptRequst(self,role, text)
    #     return inf0
    def nextProcessChat(self, msg):
        self.counter += 1
        info = singleChat.gptRequst(self,MessagesRole.USER, msg)
        return False, info
    def startProcessChat(self, pref):
        self.counter = 0
        if self.messages is not None:
            self.messages.clear()
        if pref.casefold() == "Общ".casefold() :
            text ="ты рекрутер. задавай вопросы соискателю"
            info = singleChat.gptRequst(self,MessagesRole.ASSISTANT, text)
            return False, info
        return False, None
