import os
from chatGPT import gigaChatProcessor
from commonData import mainConst
from question import questionProcessor
import userDB
import re
from qwestGenerator import *
from grade import *

from aiogram import Bot, types
from textUtilty import *

class HHreport:
    def infoUser(userInfo):
        user= userInfo[0] if userInfo[0] is not None else "Неизвестный"
        prop= userInfo[1] if userInfo[1] is not None else "неуказаны"
        msg = 'Здравствуйте '+ user
        msg = msg  + '\nВаши навыки: '+ prop
        return msg
    def getCurrentNumberTask():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path + "/result/counter.txt"
        
        counter = 0
        with open(dir_path, "r") as text_file:
            counter = text_file.readline() 

        counterInt = int(counter)+1
        with open(dir_path, "w") as text_file:
            text_file.write(str(counterInt))


        return counterInt
    def extractSkill(userInfo):
        prop= userInfo.testedUserWorks
        skills = prop.split("/")
        if len(skills)>0:
            # skills.insert(0, 'Общие')
            return skills
        return None
    def generatePrompBySkill(skill):
        msg = "Вы в режиме собеседования по вашему навыку 2" +  skill
        return msg
    
    async def infoReport(userInfo : userDB, menu, gigaChat, msgBot: types.Message):
        await msgBot.answer("Формирование отчета по собеседованию (ждите)")
        msg = "Отчет по собеседованию" + '\n' + userInfo.testedUserName + '\n' + userInfo.testedUserWorks + '\n'
        qa = userInfo.testedUserAnswers
        answers = qa.split("mode:")
        gigaChat = menu.getGigaChat()
        # генерация отчет в чат бот
        for indexAnswer, answer in enumerate(answers):
            if answer != "":
                key = answer[0]
                param = answer[1:]
                if key == 'q':
                    msg = msg + '\nВопрос: ' + param
                    
                    if indexAnswer < len(answers)-1:
                        answerNext = answers[indexAnswer+1]
                        keyNext = answerNext[0]
                        if keyNext == 'q':
                            # msg = msg + '\n<b>Ответ отсутствует</b>\n'
                            msg = msg + '\nОтвет отсутствует\n'
                    else:
                        msg = msg + '\nОтвет отсутствует\n'
                if key == 'a':
                    doAnswer = False
                    msg = msg + '\nОтвет: ' + param
                    # msg = msg + '<b>Оценка:</b>\n'
                if key == 'u':
                    msg = msg + '\nУточняющий вопрос: ' + param
                if key == 't':
                    msg = msg + '\nОтвет на уточняющий вопрос: ' + param
        
        # генерация отчет и проверка
        allQwest = 0      
        allRight = 0
        for indexAnswer, answer in enumerate(answers):
            if answer != "":
                key = answer[0]
                param = answer[1:]
                if 'Общ' not in param:
                    if key == 'q':
                        if indexAnswer < len(answers)-1:
                            answerNext = answers[indexAnswer+1]
                            # answerNext = answerNext[1:]
                            keyNext = answerNext[0]
                            if keyNext == 'a':
                                # contentSystem = "Ты опытный программист. Проверь правильность решения"
                                allQwest += 1
                                contentSystem = "Ты опытный программист"
                                contentHuman = "Реши эту задачу:\n" + param
                                RightAnswerMsg = gigaChat.gptRequst(contentSystem, contentHuman, "Решение")
                                code = HHreport.exractPartText(RightAnswerMsg)
                                if code is not None:
                                    # await msgBot.answer(code)

                                    contentHuman = "Вопрос. Это правильный ответ?:\n\"\n" + answerNext + "\n\"\n на вопрос:\n" + param + "?"
                                    # contentHuman = "Вопрос. Это правильный ответ?:\n\"\n" + code + "\n\"\n на вопрос:\n" + param + "?"
                                    # contentHuman = "Вопрос. Это правильный ответ:\n" + code + "\n на вопрос:\n" + param + "?"
                                    gradeMsg = gigaChat.gptRequst(contentSystem, contentHuman, "Оценка правльного ответа")
                                    grade = HHreport.gradeText(gradeMsg)
                                    
                                    gradeBot = f"Вопрос {allQwest} Ответ не правильный"
                                    if grade:
                                        gradeBot = f"Вопрос {allQwest} Ответ правильный"
                                        allRight += 1
                                    else:
                                        # await msgBot.answer("Правильный ответ:\n" + code)
                                        pass
                                    await msgBot.answer(gradeBot)
                                    continue
                                else:
                                    contentHuman = "Вопрос. Это правильный ответ?:\n\"\n" + answerNext[1:] + "\n\"\n на вопрос:\n" + param + "?"
                                    # contentHuman = "Вопрос. Это правильный ответ?:\n\"\n" + code + "\n\"\n на вопрос:\n" + param + "?"
                                    # contentHuman = "Вопрос. Это правильный ответ:\n" + code + "\n на вопрос:\n" + param + "?"
                                    gradeMsg = gigaChat.gptRequst(contentSystem, contentHuman, "Оценка правльного ответа")
                                    grade = HHreport.gradeText(gradeMsg)
                                    
                                    gradeBot = f"Вопрос {allQwest} Ответ не правильный"
                                    if grade:
                                        gradeBot = f"Вопрос {allQwest} Ответ правильный"
                                        allRight += 1
                                    else:
                                        # await msgBot.answer("Правильный ответ:\n" + code)
                                        pass
                                    await msgBot.answer(gradeBot)

                                    continue
                        else:
                            pass
                    if key == 'a':
                        continue
                    if key == 'u':
                        continue
                    if key == 't':
                        continue
        await msgBot.answer(f"Всего вопросов {allQwest} из них правильные {allRight}")
        return msg        
    def gradeText(text):
        test = text[:4].lower()
        if 'да' in test:
            return True
        return False
    def exractPartText(text):
        # a2 =text.partition("<code>")[2].partition("</code>")[0]
        try:
            part =text.split('<code>')[1].split('</code>')[0]
            return part
        except:
            return None
    def tagTextExtract(text):
        start = text.find('<')
        end = text.find('>', start)
        if start < 0 or end < 0:
            return None
        tag =text[start+1:end]        
        return tag
    def tagTextKill(text):
        start = text.find('<')
        end = text.find('>', start)
        if start < 0 or end < 0:
            return text
        tag =text[end+1:]        
        return tag

    async def doReport(userInfo : userDB, menu, gigaChat, msgBot: types.Message):
        task = userInfo.testedUserTask
        dir_path = os.path.dirname(os.path.realpath(__file__))
        nameFile = f"{dir_path}/result/test{task}.txt"
        # nameFile = "/home/andy/Works/aiMaindProjects/botWiseDimensions/result/test351_last.txt'"
        
        # сохранение пользователя
        userInfo.saveByName(f"{dir_path}/result/user{task}.txt")
        # userInfo.loadByName(f"{dir_path}/result/user353.txt")


        await msgBot.answer("Ждите.\nИдет формирование отчета по собеседованию")
        commonGradesShort = await HHreport.doReportToFile(userInfo, menu, gigaChat, nameFile, msgBot )
        return nameFile, commonGradesShort

    async def doReportToFile(userInfo : userDB, menu, gigaChat, nameFile, msgBot ):
        with open(nameFile, "w") as text_file:
            # инфорация о собеседнике
            text_file.write(f"Отчет N:  {userInfo.testedUserTask}\n")
            text_file.write(f"Отчет по собеседованию  {userInfo.testedUserName}\n")
            text_file.write(f"Навыки  {userInfo.testedUserWorks}\n")
        
            # отчет о навыках
            skills = HHreport.extractSkill(userInfo)
            qa = userInfo.testedUserAnswers
            answers = qa.split("mode:")
            gigaChat = menu.getGigaChat()
            qwestChat = gigaChat.getQwestChat()
            maxQwests = Grade.allGrades()

            commonGrades = []
            commonGradesShort = []
            gradeMax = Grade.maxGrades()+1
            for skill in skills:
                text_file.write(f"Собеседование по {skill}\n")
                allAnswer = 0
                allRightAnswer = 0

                # подготовка вопросов и ответов
                msgList = []
                for indexAnswer, answer in enumerate(answers):
                    if answer != "":
                        msg = None
                        key = answer[0]
                        param = answer[1:]
                        tagFull = HHreport.tagTextExtract(param)
                        tag = tagFull[1:]
                        grade = tagFull[0]
                        pureText = HHreport.tagTextKill(param)
                        
                        if skill.lower() != tag.lower():
                            continue
                        
                        if key == 'q':
                            msgList.append('q' + grade + pureText)
                        if key == 'a':
                            msgList.append('a' + grade + pureText)
                gradeCurrent = 0
                for indexQwest in range(0,len(msgList),2):
                    if len(msgList) > indexQwest+1:
                        # qwest = msgList[indexQwest]
                        # qwest = textUtility.prepareAnswer(qwest)
                        # answer = msgList[indexQwest+1]

                        qwest = msgList[indexQwest][2:]
                        answer = msgList[indexQwest+1][2:]
                        grade = msgList[indexQwest][1]

                        test = "Есть вопрос, нужно проверить правильность ответа на него:\n\""
                        test+= qwest
                        test+= "\"Вот ответ:\n\""
                        test+= answer
                        test+= "Это правильный ответ на данный вопрос?"

                        # reply, replyMsg = await HHreport.testQwestAndAnswerV1(qwest,answer, gigaChat)
                        reply, replyMsg = await HHreport.testQwestAndAnswerV0(test, gigaChat)

                        msgReply ="Правильный ответ"
                        allAnswer +=1
                        if reply:
                            allRightAnswer+=1
                            gradeCurrent += Grade.calkScaleGrade(grade)
                        else:
                            msgReply ="Неправильный ответ"
                        await msgBot.answer(msgReply)

                        
                        text_file.write(f"ВопросBot:\n\t{qwest}")
                        text_file.write(f"ОтветUser:\n\t{answer}")
                        text_file.write(f"ОтветBot:\n\t{replyMsg}")
                        text_file.write(f"\n{msgReply}\n")
                        pass
                
                msgSkill = f"\nРезультат по {skill} всего вопросов:{maxQwests} отвечено: {str(allAnswer)}  отвечено правильно: {str(allRightAnswer)}"
                commonGrades.append(msgSkill)

                msgSkill = f"\nРезультат по {skill}\n максимум: {gradeMax} набрано: {str(gradeCurrent)}"
                commonGradesShort.append(msgSkill)
            
            for common in commonGrades:
                text_file.write(common)

        return commonGradesShort
    async def testQwestAndAnswerV1(qwest,answer, gigaChat):
        chatAndy = gigaChat.chatAndy
        messages = [
            SystemMessage(
                content="Ты продвинутый продвинутый Python - Developer: Проверь решение этой задачи: \n" + qwest
            )
        ]
        info = chatAndy(messages)
        messages.append(info)
        reply = info.content
        
        messages.append(HumanMessage(content=f"Это решение правильное?: \т" + answer))
        infoApp0 = chatAndy(messages)
        
        
        if len(reply)>10:
            tt = reply[:9]
            if "Да".lower() in tt.lower():
                return True, reply
        return False, reply
        
    async def testQwestAndAnswerV0(quest, gigaChat):
        chatAndy = gigaChat.chatAndy
        messages = [
            SystemMessage(
                content=quest
            )
        ]
        info = chatAndy(messages)
        messages.append(info)
        reply = info.content
        if len(reply)>10:
            tt = reply[:9]
            if "Да".lower() in tt.lower():
                return True, reply
        return False, reply
        
