class textUtility:
    # ограничить ответ до первого вхождения слов  borderKey
    def rangeAnswer(msg, borderKey):
        index = msg.lower().find(borderKey.lower())
        if index > 0:
            return msg[:index]
        return msg
    # подготовка ответа на вывод удалениее ненужных слов
    def prepareAnswer(msg):
        if msg is None:
            return "None"
        index = msg.lower().find(":")
        if index > 0:
            msgNex = msg[index+1:]
            
            index = msgNex.lower().find("Правильный ответ:".lower())
            if index > 0:
                msgNex = msgNex[:index]
            index = msgNex.lower().find("Ответ:".lower())
            if index > 0:
                msgNex = msgNex[:index]
            return msgNex
        return msg
