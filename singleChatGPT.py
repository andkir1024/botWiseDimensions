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
    # ?сформулируй вопрос другими словами
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
            # еще придумай задачу из Дональд Кнута и реши ее на питоне
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
            self.messages.append(info)
            return False, "[" + self.pref + "] " + info.content
        else:
            task = self.pref
            self.messages = [
                SystemMessage(
                    # еще придумай задачу из Дональд Кнута и реши ее на питоне
                    content=f"Ты строгий бот-рекрутер, который ищет кандидата на роль ведущего программиста. Придумай соискателю сложную вопрос по {task}. Я опытный программист"
                )
            ]
            info = self.chatAndy(self.messages)
            self.messages.append(info)
            return False, "[" + self.pref + "] " + info.content
        return False, None

    # 111111111111111111111111111111
    def startChat(self, quest):
        self.counter = 0
        if self.messages is not None:
            self.messages.clear()
        task = self.pref
        self.messages = [
            SystemMessage(
                content=quest
            )
        ]
        info = self.chatAndy(self.messages)
        self.messages.append(info)
        return info.content
    def nextChat(self, msg):
        # self.messages = [
        #     SystemMessage(
        #         content=msg
        #     )
        # ]
        # info = self.chatAndy(self.messages)
        # self.messages.append(info)
        # return info.content

        self.counter += 1
        
        # self.messages.append(HumanMessage(content="Придумай соискателю еще вопрос по теории"))
        # self.messages.append(HumanMessage(content="Продолжай придумывать следующий вопрос"))
        # self.messages.append(HumanMessage(content="придумай еще задачу по программированию в области Математика и теория графов."))
        # self.messages.append(HumanMessage(content="придумай еще одну задачу по программированию в области Математика и теория графов."))
        # self.messages.append(HumanMessage(content="Python Developer: вопрос для собеседования"))

        # self.messages.append(HumanMessage(content="Python Developer: придумай еще один другой вопрос для собеседования"))
        self.messages.append(HumanMessage(content="Python Developer: придумай еще одну задачу для собеседования на Python и реши ее"))


        # self.messages.append(SystemMessage(content="придумай еще задачу."))
        info = self.chatAndy(self.messages)
        self.messages.append(info)
    
        self.counter += 1
        return info.content
