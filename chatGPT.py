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

from singleChatGPT import *

# Авторизация в сервисе GigaChat
andyCred = "MTI3YzYzN2ItOGIwOC00NDNiLWJmOGItOGM3N2NmNTYxMjZhOjVjYWYxMjljLWJlMjEtNDQ4Yi05M2Q5LTI1N2ZhMmEzMmU2Mw=="
keyWorlds = [["Python","0"],["Java","1"],["PHP","2"],["C++","3"]]

class gigaChatProcessor:
    def __init__(self):
        self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False)
        # self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, temperature=2)
        self.counterChatCommon = 0
        self.counterChat = 0
        self.isFinishCommonChat = True
        self.commomChat = singleChat(self.chatAndy)
        self.techChat = singleChat(self.chatAndy)
        self.keyAdded = None
        return
    def testKey(self, testedUserWorks):
        keyAdded = []
        for key in keyWorlds:
            if key[0].lower() in testedUserWorks.lower():
                keyAdded.append(key)
                
        return keyAdded
   
    def gptRequstVer1(self, roleReuest, requestMsg):
        messages = [
            SystemMessage(
                role = roleReuest,
                # temperature = 2,
                # content="придумать сложный вопрос по Python с примером"
                # content="Напиши 3 вопроса для senior Python"
                # content="Ты рекрутер по senior Python. Напиши 3 вопроса"
                # content="Напиши 5 вопросов по Python"
                # content="Ты рекрутер Напиши 3 вопроса"
                # content="Составить вопросы senior-java"
                # content="что такое def в python"
                content=requestMsg
            )
        ]
        res =self.chatAndy(messages)
        # messages.append(res)
        # self.counter += 1
        return res.content         
        
    def gptRequst(self, contentSystem, contentHuman, printMsg):
        messages = [
            SystemMessage(
                content=contentSystem
            ),
            HumanMessage(content=contentHuman),
        ]
        Msg= self.chatAndy(messages)
        print("\n" + printMsg + "\n"+Msg.content)
        return Msg.content


    def doFullGptRequstVer2(self, key):
        AskMsg = "Вопрос"
        RightAnswerMsg = "Правильный ответ на вопрос"
        LevelMsg = "Ответ на вопрос"

        inf1 = None
        inf2 = None
        
        role = MessagesRole.ASSISTANT
        # text ="Придумай задачу к собеседованию по Python +sql"
        text ="Придумай соискателю сложную вопрос по OpenGL. Я опытный программист"
        
        inf0 = gigaChatProcessor.gptRequstVer1(self,role, text)
        # inf1 = gigaChatProcessor.gptRequstVer1(self,role, text)
        # inf2 = gigaChatProcessor.gptRequstVer1(self,role, text)

        return inf0, inf1 , inf2, None

    def start(self, keyAdded, msg):
        self.counterChat += 1
        self.keyAdded = keyAdded
        if self.counterChat == 1:
            self.isFinishCommonChat, info = self.commomChat.startProcessChat("Общ", True)
            return info, -1, None , None, None
        else:
            if self.isFinishCommonChat == False:
                test, info = self.commomChat.nextProcessChat(msg)
                return info, -1, None , None, None
            else:
                pass
                return info, -1, None , None, None
            # lenKey = len(keyAdded)
            # indexKey = random.randint(0,lenKey-1)
            # prefReq =""
            # AskMsg, RightAnswerMsg , LevelMsg, BadLevelMsg = gigaChatProcessor.doFullGptRequstVer2(self, "key");
            # return prefReq + AskMsg, indexKey, RightAnswerMsg , LevelMsg, BadLevelMsg
    def finishCommon(self):
        self.isFinishCommonChat = True
        lenKey = len(self.keyAdded)
        indexKey = random.randint(0,lenKey-1)
        prefReq =self.keyAdded[indexKey][0]
        notMaind, info = self.commomChat.startProcessChat(prefReq, False)
        return info, -1, None , None, None
