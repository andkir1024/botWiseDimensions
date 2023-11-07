import json
from jsoncomment import JsonComment
from aiogram import types
from kbs import *
from processorQR import *

class testBotUtils:
    stop = False
    
    async def testManager(msg: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(msg)
        if isNew == False:
            pieces = msg.text.split()
            if len(pieces)==2:
                mode = pieces[1]
                if mode == '0':
                    await testBotUtils.testCreateRequest(userInfo, msg)
                if mode == '1':
                    await testBotUtils.testQR(userInfo, msg)
                return
            else:
               await msg.answer("Небходим номер запроса")

    # тестирование QR кодов
    async def testQR(userInfo,msg: types.Message):
        global stop
        try:
            stop = False
            name = mainConst.DIR_TEST + "test.jsonc"
            parser = JsonComment(json)
            with open(name, 'r', encoding='utf-8') as f: #открыли файл с данными
                parsed_object = parser.load(f)
            allTest = parsed_object['allTests']
            for all in allTest:
                if all['typeTest'] == 'qrTests':
                    for test in all['tests']:
                        id = test['id']
                        dir = test['dir']
                        data = test['data']
                        param = int(test['param'])
                        await msg.answer(f"Тестировиние {id}")
                        allTested = 0
                        for photo in data:
                            name = photo['name']
                            qr = photo['qr']
                            allTested +=1
                            if stop == True:
                                await msg.answer(f"Всего {allTested}")
                                return
                            photo_name = mainConst.DIR_TEST + dir + "/" + name
                            resultQR = decodeImage(photo_name, param)
                            for res in resultQR:
                                await msg.answer(res)
                        await msg.answer(f"Всего {allTested}")
        except:
            await msg.answer("Ошибка в тестировании")



