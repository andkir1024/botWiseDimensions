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
from qwestGenerator import *

# Авторизация в сервисе GigaChat
andyCred = "MTI3YzYzN2ItOGIwOC00NDNiLWJmOGItOGM3N2NmNTYxMjZhOjVjYWYxMjljLWJlMjEtNDQ4Yi05M2Q5LTI1N2ZhMmEzMmU2Mw=="
# p прогорапммирование
# d технология
# keyWorlds = [["Python1","p"],["PHP1","p"],["C++","p"],
#              ["Yii2","d"],["PostgreSQL","d"],["Big Data","d"],
#              ["OpenGL","d"],["OpenCM","d"],["C#","p"],
#              ["MySQL","d"],["Docker","d"],["Git","d"],["REST","d"]]

keyWorlds = [["Python","p"],["Java","p"],["PHP","p"],["C++","p"],
             ["JavaScript","p"],["Yii2","d"],["PostgreSQL","d"],
             ["OpenGL","d"],["OpenCM","d"],["C#","p"],
             ["MySQL","d"],["Docker","d"],["Git","d"],["REST","d"]]

class gigaChatProcessor:
    def __init__(self):
        # self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False)
        # self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, temperature=0.5)
        # self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, temperature=2, max_tokens=2024)


        self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, temperature=2, n=3)


        # self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, temperature=1.5)
        # self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, max_tokens=2024, temperature=2)
        # self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, max_tokens=2024)
        self.counterChatCommon = 0
        self.counterChat = 0
        self.isFinishCommonChat = True
        self.commomChat = singleChat(self.chatAndy)
        self.techChat = singleChat(self.chatAndy)
        self.qwestChat = qwestGenator(self.chatAndy)
        self.keyAdded = None
        return
    def getQwestChat(self):
        return self.qwestChat
    def testKey(self, testedUserWorks):
        keyAdded = []
        for key in keyWorlds:
            if key[0].lower() in testedUserWorks.lower():
                keyAdded.append(key)
                
        return keyAdded
    # проверка доступен ли данный навык прогрнамме
    def testSkill(self, skill):
        for key in keyWorlds:
            if key[0].lower() in skill.lower():
                return True
                
        return False
   
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

    def prepare(self):
        self.counterChatCommon = 0
        self.counterChat = 0
        self.isFinishCommonChat = True
        self.qwestChat.prepareQwest()
        pass
    def requestStep(self, keyAdded, msg):
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
                # test, info = self.commomChat.nextProcessChat(msg)
                info,a1,a2,a3,a4 = self.finishCommon()
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
        notMaind, info = self.techChat.startProcessChat(prefReq, False)
        return info, -1, None , None, None
    def nextTech(self, msg):
        notMaind, info = self.techChat.nextProcessChat(msg)
        return info, -1, None , None, None
    
    def nextQwest(self, msg, number, skill, isFirst, userInfo):
        # нахождение сврйства скила
        findedKey = None
        if skill is not None:
            for key in keyWorlds:
                if key[0] == skill:
                    findedKey = key
                    break
        if findedKey is not None:
            return self.qwestChat.nextQwest(number, skill, findedKey, isFirst, userInfo)
        else:
            return 0, "Навык не обрабатывается", "Навык не обрабатывается"
        # grade = 0
        # if number > 2:
        #     grade = 1
        # if number > 4:
        #     grade = 2
        # if number > 6:
        #     grade = 3
        # if number > 8:
        #     grade = 4
        # # if number > 10:
        # if number > 3:
        #     grade = None
        # if skill is not None:
        #     Ask = self.createQwest(grade, key, number)
        #     NextAsk  = f"Вопрос N:{number} {gigaChatProcessor.decodeGrade(grade) }\n{Ask}"
        #     return grade, NextAsk
        # return grade, ""
    # def createQwest(self, grade, key, number):
    #     quest = "Ты продвинутый Python Developer: одна случайная сложная задача для собеседования по Python и реши ее"

    #     if number == 0:
    #         info = self.techChat.startChat(quest)
    #     else:
    #         # info = self.techChat.startChat(quest)
    #         info = self.techChat.nextChat(quest)
    #     return info
    #     # answer = self.rangeAnswer(info,"правильный")
    #     # answer = self.rangeAnswer(answer,"пример")
    #     # answer = self.rangeAnswer(answer,"решение")
    #     # return answer
    # ограничить ответ до первого вхождения слов  borderKey
    def rangeAnswer(self, msg, borderKey):
        index = msg.lower().find(borderKey.lower())
        if index > 0:
            return msg[:index]
        return msg

