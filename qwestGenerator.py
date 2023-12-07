import random
import re
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
from textUtilty import *
from grade import *

class qwestGenator:
    def __init__(self, gigaChat):
        self.chatAndy = gigaChat
        self.counterChat = 0
        self.messages = None
        return
    # подготовка к началу создания вопросов по всем темам
    # prepareQwest первый вызов на соискателя
    # nextQwest    при согласии по опросу данного навыка вызывается (isFirst true значит первый вопрос по данному skill)
    # createQwest вызывается в nextQwest и там собственно создается вопрос
    def prepareQwest(self):
        self.counterChat = 0
        pass
    # isFirst true значит первый вопрос по данному skill
    def nextQwest(self, number, skill, key, isFirst, userInfo):
        grade = Grade.calkGradeVer(number)
        if isFirst:
            self.skill = skill
            allNumber = Grade.allGrades()
            # allNumber = 30
            allQwest = self.doMassQuest(grade, key, int(allNumber/3))
            singleQwest = self.selectQuest(grade, allQwest, 0)
            userInfo.testedCurrentRequsts = 0
            singleQwest  = f"Вопрос N:{number} {Grade.decodeGrade(grade) }\n{textUtility.prepareAnswer(singleQwest)}"
            return grade, allQwest, singleQwest
        else:
            userInfo.testedCurrentRequsts += 1
            singleQwest = self.selectQuest(grade, userInfo.testedAllRequsts, userInfo.testedCurrentRequsts)
            if singleQwest is None:
                return None, "" , ""
            singleQwest  = f"Вопрос N:{number} {Grade.decodeGrade(grade) }\n{textUtility.prepareAnswer(singleQwest)}"
            return grade, singleQwest, singleQwest
        '''
        if skill is not None:
            Ask = self.createQwest(grade, key, number)
            NextAsk  = f"Вопрос N:{number} {Grade.decodeGrade(grade) }\n{Ask}"
            PureAsk  = f"Вопрос N:{number} {Grade.decodeGrade(grade) }\n{textUtility.prepareAnswer(Ask)}"
            return grade, Ask, Ask
            # return grade, NextAsk, PureAsk
        '''
        return grade, "", ""
    def createQwest(self, grade, key, number):
        skill = key[0]
        place = key[1]
        prompt = ""
        appCondition  = ""
        if place == 'p':
            prompt = f"Ты продвинутый {skill} - Developer: "
            appCondition  = " Не решай эту задачу"
        if place == 'd':
            prompt = f"Ты продвинутый эксперт в {skill}: "
            appCondition  = " Не печатай ответ"
            
        quest = f"Один случайный вопрос для собеседования по {skill} по теории языка"
        if grade == 1:
            quest = f"Один случайный вопрос для собеседования по {skill} по алгоритмам"
        elif grade == 2:
            quest = prompt + f"Один случайный вопрос для собеседования по {skill} по кодированию"
        elif grade == 3:
            quest = prompt + f"один случайный сложный вопрос для собеседования по {skill} по кодированию на этом языке"
        elif grade == 4:
            quest = prompt + f"придумай еще одну случайную более сложную задачу для собеседования по {skill}." + appCondition
        # quest = "Ты продвинутый Python - Developer: придумай 5 случайных и более сложных задач для собеседования по Python. Каждая слудующая задача должна быть сложнее предидущей"
        quest = "Ты продвинутый Python - Developer: придумай 5 олимпиадных сложных задач для собеседования по Python"
        quest = "Ты продвинутый Python - Developer. Придумай 10 случайных и более сложных задач для собеседования по Python."
        quest = "Ты продвинутый Python - Developer. Придумай 10 случайных и более сложных вопросов по теории языка для собеседования по Python."
        # quest = prompt + f"один случайный более сложный вопрос для собеседования по {skill} по теории" + appCondition
        # quest = prompt + f"один случайный более сложный вопрос для собеседования по {skill} по алгоритмам" + appCondition
        # quest = prompt + f"один случайный более сложный вопрос для собеседования по {skill} по кодированию" + appCondition
        # quest = prompt + f"одна случайная более сложная задача для собеседования по {skill} и ее решение" + appCondition
        # quest = prompt + f"придумай еще одну случайную более сложную задачу для собеседования по {skill}." + appCondition
        # quest = prompt + f"придумай еще одну случайную более сложную задачу для собеседования по {skill} без обьяснений и решений." + appCondition
        
        # quest = prompt + f"придумай еще одну случайную более сложную задачу для собеседования по {skill}. Реши эту задачу"
        # self.messages.append(HumanMessage(content="Ты продвинутый Python Developer: придумай еще одну более сложную задачу для собеседования на Python и реши ее"))

        info = self.startChat(quest)
        # if number == 0:
        #     info = self.startChat(quest)
        # else:
        #     info = self.nextChat(quest)
        return info
    def selectQuest(self, grade, allQwest, border):
        # finded = re.search(r'\d+.', allQwest)
        # finded = re.findall(r'\d+.', allQwest)
        finded = re.split(r'\d+.', allQwest)
        
        zz = allQwest.replace(".", "JJ")
        finded = re.split(r"1JJ|2JJ|3JJ|4JJ|5JJ|6JJ|7JJ|8JJ|9JJ|0JJ", zz)

        for index, qwest in enumerate(finded):
            # if qwest != '' and index >= border-1:
            if qwest != '' and index > border:
                qwestPure = qwest.replace("JJ", ".")
                return qwestPure
        return None
    def doMassQuest(self, grade, key, allNumber):
        allNumber += 1
        skill = key[0]
        place = key[1]
        prompt = ""
        quest = ""
        questTheory = ""
        if place == 'p':
            prompt = f"Ты продвинутый {skill} - Developer: "
            quest = prompt + f"Придумай {allNumber} случайных и более сложных задач для собеседования по {skill}."
            questTheory = prompt + f"Придумай {allNumber} случайных и более сложных вопросов по теории языка для собеседования по {skill}."
        if place == 'd':
            prompt = f"Ты продвинутый эксперт в {skill}: "
            quest = prompt + f"Придумай {allNumber} случайных и более сложных задач для собеседования по {skill}."
            questTheory = prompt + f"Придумай {allNumber} случайных и более сложных вопросов по теории {skill}."

        if self.messages is not None:
            self.messages.clear()
        self.messages = [
            SystemMessage(
                content=quest
            )
        ]
        infoStart = self.chatAndy(self.messages)
        self.messages.append(infoStart)
        
        self.messages.append(HumanMessage(content=f"придумай еще {allNumber} случайных и более сложных задач для собеседования по программированию на {skill}"))
        infoApp0 = self.chatAndy(self.messages)
        self.messages.append(infoApp0)

        # self.messages.append(HumanMessage(content="придумай еще {allNumber} случайных и более сложных задач для собеседования по программированию на {skill}"))
        # infoApp1 = self.chatAndy(self.messages)
        # self.messages.append(infoApp1)
        
        # вопросы по теории
        self.messages.clear()
        self.messages = [
            SystemMessage(
                content=questTheory
            )
        ]
        infoTheory = self.chatAndy(self.messages)
        outMsg = infoTheory.content + "\n" + infoStart.content + "\n" + infoApp0.content
        # outMsg = infoTheory.content + "\n" + infoStart.content + "\n" + infoApp0.content + "\n" + infoApp1.content

        return outMsg
    # начало и инициализация  gigaChat
    def startChat(self, quest):
        # return "only test"
        if self.messages is not None:
            self.messages.clear()
        self.messages = [
            SystemMessage(
                content=quest
            )
        ]
        info = self.chatAndy(self.messages)
        self.messages.append(info)
        # return info.content
        
        outMsg = info.content + "\nОТВЕТ:\n"
        # self.messages.append(HumanMessage(content="Дай ответ на этот вопрос: " + textUtility.prepareAnswer(info.content)))
        self.messages.append(HumanMessage(content="придумай еще 10 случайных и более сложных задач для собеседования по Python"))
        info = self.chatAndy(self.messages)
        self.messages.append(info)
        outMsg += info.content
        return outMsg
    # последовательные шаги в gigaChat
    def nextChat(self, msg):
        self.messages.append(HumanMessage(content=msg))
        # self.messages.append(HumanMessage(content="Ты продвинутый Python Developer: придумай еще одну более сложную задачу для собеседования на Python и реши ее"))
        info = self.chatAndy(self.messages)
        self.messages.append(info)
        return info.content
