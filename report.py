from question import questionProcessor
import userDB


class HHreport:
    def infoUser(userInfo):
        msg = 'Здравствуйте '+ userInfo[0] if not None else "Неизвестный"
        msg = msg  + '\nВаши навыки: '+ userInfo[1] if not None else "неуказаны"
        return msg

    def infoReport(userInfo : userDB, menu):
        msg = "Отчет по собеседованию" + '\n' + userInfo.testedUserName + '\n' + userInfo.testedUserWorks + '\n'
        qa = userInfo.testedUserAnswers
        answers = qa.split("mode:")
        for answer in answers:
            if answer != "":
                key = answer[0]
                param = answer[1:]
                if key == 'q':
                    index = int(param)
                    msqQuest = questionProcessor.get_quest_byId(menu, index)['qwest']
                    msg = msg + '\nВопрос: ' + msqQuest

                    msqAnswer = questionProcessor.get_quest_byId(menu, index)['answer']
                    msqAnswer = msqAnswer.replace("\\n", "\n")
                    msg = msg + '\nПравильный ответ: ' + msqAnswer
                    
                if key == 'a':
                    msg = msg + '\nОтвет: ' + param
        return msg    