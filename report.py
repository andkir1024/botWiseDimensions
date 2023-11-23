from question import questionProcessor
import userDB


class HHreport:
    def infoUser(userInfo):
        user= userInfo[0] if userInfo[0] is not None else "Неизвестный"
        prop= userInfo[1] if userInfo[1] is not None else "неуказаны"
        msg = 'Здравствуйте '+ user
        msg = msg  + '\nВаши навыки: '+ prop
        return msg

    def infoReport(userInfo : userDB, menu):
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
                            msg = msg + '\n<b>Ответ отсутствует\nОценка: плохо</b>\n'
                    else:
                        msg = msg + '\n<b>Ответ отсутствует</b>\n'
                if key == 'a':
                    doAnswer = False
                    msg = msg + '\n<b>Ответ:</b> ' + param
                    msg = msg + '<b>Оценка:</b>\n'
        return msg    