class HHreport:
    def infoUser(userInfo):
        msg = 'Здравствуйте '+ userInfo[0] if not None else "Неизвестный" + "\n"
        msg = msg + 'Ваши навыки: '+ userInfo[1] if not None else "неуказаны" + "\n"
        return msg