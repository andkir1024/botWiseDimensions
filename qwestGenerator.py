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
from textUtilty import *

class qwestGenator:
    def __init__(self, gigaChat):
        self.chatAndy = gigaChat
        self.counterChat = 0
        self.messages = None
        return
    def calkGradeVer2(number):
        grade = 0
        if number > 5:
            grade = 1
        if number > 10:
            grade = 2
        if number > 15:
            grade = 3
        if number > 25:
            grade = 4
        if number > 30:
            grade = None
        return grade
    def calkGradeVer1(number):
        grade = 0
        if number > 2:
            grade = 1
        if number > 4:
            grade = 2
        if number > 6:
            grade = 3
        if number > 8:
            grade = 4
        if number > 10:
            grade = None
        return grade
    def decodeGrade(grade):
        if grade is None:
            return "_"
        return str(grade)
    def decodeGradeSimbole(grade):
        if grade is None:
            return "_"
        match int(grade):
            case 0:
                return "Junior"
            case 1:
                return "Junior+"
            case 2:
                return "Middle"
            case 3:
                return "Middle+"
            case 4:
                return "Senior"
        return "+"
    def allGrades(self):
        for num in range(1,100):
            grade, NextAsk = self.nextQwest(None, num, None)
            if grade is None:
                return num-1
        return 0
    # подготовка к началу создания вопросов по всем темам
    # prepareQwest первый вызов на соискателя
    # nextQwest    при согласии по опросу данного навыка вызывается (isFirst true значит первый вопрос по данному skill)
    # createQwest вызывается в nextQwest и там собственно создается вопрос
    def prepareQwest(self):
        self.counterChat = 0
        pass
    # isFirst true значит первый вопрос по данному skill
    def nextQwest(self, number, skill, key, isFirst):
        if isFirst:
            self.skill = skill
        grade = qwestGenator.calkGradeVer1(number)
        if skill is not None:
            Ask = self.createQwest(grade, key, number)
            NextAsk  = f"Вопрос N:{number} {qwestGenator.decodeGrade(grade) }\n{Ask}"
            PureAsk  = f"Вопрос N:{number} {qwestGenator.decodeGrade(grade) }\n{textUtility.prepareAnswer(Ask)}"
            return grade, NextAsk, PureAsk
        return grade, "", ""
    def createQwest(self, grade, key, number):
        skill = key[0]
        place = key[1]
        prompt = ""
        appCondition  = ""
        if place == 'p':
            prompt = f"Ты продвинутый {skill} Developer: "
            appCondition  = " Не решай эту задачу"
        if place == 'd':
            prompt = f"Ты продвинутый эксперт в {skill}: "
            appCondition  = " Не печатай ответ"
            
        quest = f"один случайный вопрос для собеседования по {skill} по теории языка"
        if grade == 1:
            quest = f"один случайный вопрос для собеседования по {skill} по алгоритмам"
        elif grade == 2:
            quest = f"один случайный вопрос для собеседования по {skill} по алгоритмам"
        elif grade == 3:
            quest = prompt + f"один случайный сложный вопрос для собеседования по {skill} по кодированию на этом языке"
        else:
            quest = prompt + f"придумай еще одну случайную более сложную задачу для собеседования по {skill}." + appCondition
        
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
    # начало и инициализация  gigaChat
    def startChat(self, quest):
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
        # outMsg =info.content + "\nОТВЕТ:\n"
        self.messages.append(HumanMessage(content="Дай ответ на этот вопрос: " + textUtility.prepareAnswer(info.content)))
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
