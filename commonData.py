from aiogram import types
import enum

class mainConst():
    API_TOKEN = '6905645245:AAEBMB_c9FvLE2I2xjN6CVOinATPlmEKjn4'    
    DB_TEST = True
    OKDESK_TOKEN = 'api_token=ae71c1f696464efe94383d6acf37fa031b1848fb'
    DIR_DATA = '/data/'
    DIR_USER = '/users/'
    DIR_RESOURCE = '/resource/'
    DIR_TEST = './testData/'
    

class infoShow(int,enum.Enum):
    undifined = -1
    QR = 1

class decodeQRMode(int,enum.Enum):
    onlyQR = -1
    MTC = 0
    Vimpel = 1
    MVideo = 2
    MegaFon = 3
    Paper = 4

class userRight(str,enum.Enum):
    undifined = 'undifined'
    admin = 'admin'
    worker = 'worker'
    user = 'user'

class userType(str,enum.Enum):
    undifined = 'undifined'
    admin = 'admin'
    employer = 'employer'
    client = 'client'
    clientAntiFrod = 'clientAntiFrod'
    clientIntegration = 'clientIntegration'

class userAssistant(str, enum.Enum):
    undifined = 'undifined'
    assistant0 = 'assistant0'
    assistant1 = 'assistant1'
    assistant2 = 'assistant2'
