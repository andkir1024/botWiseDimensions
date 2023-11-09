import userDB


class HHreport:
    def infoUser(userInfo):
        msg = 'Здравствуйте '+ userInfo[0] if not None else "Неизвестный"
        msg = msg  + '\nВаши навыки: '+ userInfo[1] if not None else "неуказаны"
        return msg

    def infoReport(userInfo : userDB):
        msg = "Отчет по собеседованию" + '\n' + userInfo.testedUserName + '\n' + userInfo.testedUserWorks
        return msg    