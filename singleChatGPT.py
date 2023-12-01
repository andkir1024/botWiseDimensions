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
        self.pref = ""

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
        # info = singleChat.gptRequst(self,MessagesRole.USER, msg)
        
        self.messages.append(HumanMessage(content=msg))
        info = self.chatAndy(self.messages)
        self.messages.append(info)
    
        self.counter += 1
        return False, "[" + self.pref + "] " + info.content
    def startProcessChat(self, pref, continuedChat):
        self.counter = 0
        self.pref = pref
        self.continuedChat = continuedChat
        if self.messages is not None:
            self.messages.clear()
        if pref.casefold() == "Общ".casefold() :
            # text ="ты рекрутер. задавай вопросы соискателю"
            # info = singleChat.gptRequst(self,MessagesRole.ASSISTANT, text)
            
            self.messages = [
                SystemMessage(
                    content="Ты строгий бот-рекрутер, который ищет кандидата на роль ведущего программиста. Задавай вопросы соискателю по работе"
                    # content="Ты ищешь кандидата на роль ведущего программиста. Задавай вопросы соискателю по работе"
                    # content="Ты рекрутер. Ты ищешь кандидата на роль ведущего программиста. Задавай вопросы соискателю"
                    # content="Ты рекрутер. Ты ищешь программиста Python. Задавай вопросы соискателю"
                    # content="ты рекрутер. задавай вопросы соискателю"
                    # content="ты рекрутер, который задавет вопросы соискателю"
                    # content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
                )
            ]
            info = self.chatAndy(self.messages)
            return False, "[" + self.pref + "] " + info.content
        else:
            self.messages = [
                SystemMessage(
                    content="Ты строгий бот-рекрутер, который ищет кандидата на роль ведущего программиста. Задавай вопросы соискателю по работе"
                )
            ]
            info = self.chatAndy(self.messages)
            return False, "[" + self.pref + "] " + info.content
        return False, None
