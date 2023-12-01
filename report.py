from question import questionProcessor
import userDB
import re

from aiogram import Bot, types

class HHreport:
    def infoUser(userInfo):
        user= userInfo[0] if userInfo[0] is not None else "Неизвестный"
        prop= userInfo[1] if userInfo[1] is not None else "неуказаны"
        msg = 'Здравствуйте '+ user
        msg = msg  + '\nВаши навыки: '+ prop
        return msg

    def infoReport1(userInfo : userDB, menu):
        msg = "<b>Отчет по собеседованию</b>" + '\n' + userInfo.testedUserName + '\n' + userInfo.testedUserWorks + '\n'
        qa = userInfo.testedUserAnswers
        answers = qa.split("mode:")
        for indexAnswer, answer in enumerate(answers):
            if answer != "":
                key = answer[0]
                param = answer[1:]
                if key == 'q':
                    # index = int(param)
                    # msqQuest = questionProcessor.get_quest_byId(menu, index)['qwest']
                    # msg = msg + '\n<b>Вопрос:</b> ' + msqQuest
                    msg = msg + '\n<b>Вопрос:</b> ' + param

                    # msqAnswer = questionProcessor.get_quest_byId(menu, index)['answer']
                    # msqAnswer = msqAnswer.replace("\\n", "\n")
                    # msg = msg + '\n<b>Правильный ответ:</b> ' + msqAnswer
                    
                    if indexAnswer < len(answers)-1:
                        answerNext = answers[indexAnswer+1]
                        keyNext = answerNext[0]
                        if keyNext == 'q':
                            # msg = msg + '\n<b>Ответ отсутствует</b>\n'
                            msg = msg + '\n<b>Ответ отсутствует\nОценка: плохо</b>\n'
                    else:
                        msg = msg + '\n<b>Ответ отсутствует</b>\n'
                if key == 'a':
                    doAnswer = False
                    msg = msg + '\n<b>Ответ:</b> ' + param
                    # msg = msg + '<b>Оценка:</b>\n'
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
                            keyNext = answerNext[0]
                            if keyNext == 'a':
                                # contentSystem = "Ты опытный программист. Проверь правильность решения"
                                allQwest += 1
                                contentSystem = "Ты опытный программист"
                                contentHuman = "Реши эту задачу:\n" + param
                                RightAnswerMsg = gigaChat.gptRequst(contentSystem, contentHuman, "Решение")
                                code = str(HHreport.exractPartText(RightAnswerMsg))
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
        # start = text.find('<code>') + 6
        # end = text.find('</code>', start)
        # a3 =text[start:end]

        # m = re.search('<code>(.+?)</code>', text)
        # if m:
        #     found = m.group(1)
        #     return found
        # return None