import json
from commonData import *
from aiogram import types
import os.path
import codecs

class user:
    id : int
    phone : str
    first_name : str
    last_name : str
    mode : int
    right : userRight
    assistant : userAssistant
    current_menu : str
    data : str
    userType : str
    counter : int
    urlUser : str
    # информация выводимая ботом для конкретного пользователя
    infoMode : int
    testedUserName : str
    testedUserWorks : str
    testedUserAnswers : str
    testedUserMode : str
    testedUserQuestId : int
    testedUserTask : int
    testedUserQuestCounter : int
    testedUserQuestName : str
    testedCurrentRequsts : int
    testedAllRequsts : str
    def __init__(self):
        self.id = 1335723885
        self.phone = '89218866929'
        self.first_name = 'Андрей'
        self.last_name = 'Кирилов'
        self.mode = -1
        self.right = userRight.admin
        self.assistant = userAssistant.assistant0
        self.current_menu = ""
        self.data = ""
        self.infoMode = infoShow.undifined
        self.userType = userType.client
        self.counter = -1
        self.urlUser = ""
        self.testedUserName = ""
        self.testedUserWorks = ""
        self.testedUserAnswers = ""
        self.testedUserMode = ""
        self.testedUserQuestId = -1
        self.testedUserTask = 0
        self.testedUserQuestCounter = 0
        self.testedUserQuestName = ""
        self.testedCurrentRequsts = 0
        self.testedAllRequsts = ""

    def __init__(self, message : types.Message):
        from_user = message.from_user
        self.id = from_user.id
        self.phone = None
        self.first_name = from_user.first_name
        self.last_name = from_user.last_name
        self.mode = -1
        self.right = userRight.user
        self.assistant = userAssistant.assistant0
        self.current_menu = ""
        self.data = ""
        self.infoMode = infoShow.undifined
        self.userType = userType.client
        self.counter = -1
        self.urlUser = ""
        self.testedUserName = ""
        self.testedUserWorks = ""
        self.testedUserAnswers = ""
        self.testedUserMode = ""
        self.testedUserQuestId = -1
        self.testedUserTask = 0
        self.testedUserQuestCounter = 0
        self.testedUserQuestName = ""
        self.testedCurrentRequsts = 0
        self.testedAllRequsts = ""
        
    def save(self, clearCounter = True):
        if clearCounter:
            self.counter = -1

        s = json.dumps(self.__dict__)
        str16 = str(s)
        # s16 = str16.decode("utf-8")
        
        # utf16_string = string.encode("utf-16")
        # utf16_string = str16
        # string = utf16_string.decode("utf-16")
        
        fileUser = user.getFileName(self.id)
    
       
        # with codecs.open(fileUser, "w", "utf-16") as text_file:
        #     text_file.write(str(s))

        # with open(fileUser, "w", encoding="utf-16") as text_file:
        with open(fileUser, "w") as text_file:
            text_file.write(str(s))
        return
    def saveByName(self, fileUser):
        s = json.dumps(self.__dict__)
        with open(fileUser, "w") as text_file:
            text_file.write(str(s))
    def loadByName(self, fileUser):
        exists = os.path.exists(fileUser)
        if exists:
            f = open(fileUser)
            try:
                data = json.load(f)
                self.__dict__ = data
            except:
                pass
            try:
                aa = self.counter
            except:
                exec("self.counter=-1")
            return
        return

    def load(self):
        fileUser = user.getFileName(self.id)
        exists = os.path.exists(fileUser)
        if exists:
            f = open(fileUser)
            try:
                data = json.load(f)
                self.__dict__ = data
            except:
                pass
            try:
                aa = self.counter
            except:
                exec("self.counter=-1")
            return
        return

    def getFileName(id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileUser = dir_path + mainConst.DIR_USER + str(id) + '.json'
        return fileUser
        
        
class userDB:
    def __init__(self, isModel):
        self.isModel = isModel
        return
    def getUserInfo(self, message : types.Message):
        if mainConst.DB_TEST:
            return self.getTestUserInfo(message)
        return None, None
    def getTestUserInfo(self, message : types.Message):
        id = message.from_id
        fileUser = user.getFileName(id)
        exists = os.path.exists(fileUser)
        if exists:
            usr =  user(message)
            usr.load()
            return usr, False
        # новый пользователь (сохранить, создать)
        usr =  user(message)
        usr.save()
        return usr, True
