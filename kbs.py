import html
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize
from doHHresume import HHresume
from managerQR import managerQR
from processorMenu import *
from aiogram.types import InputFile
from question import questionProcessor

from report import HHreport


from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions

class kbs:
    def get_kb_phone(menu, msg: types.Message) -> ReplyKeyboardMarkup:
        kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
        b2 = KeyboardButton('Зарегистрироваться', request_contact=True)
        kb_clients.add(b2)
        return kb_clients, 'Для начала работы нам нужно зарегистрироваться', 'menuPhone' 

    def get_kb(menu, msg: types.Message, userInfo, isNew) -> ReplyKeyboardMarkup:
        msgCmd = msg.text
        first = msgCmd[0]
        if first == '/':
            msgCmd = msgCmd[1:]
        # if isNew:
        #     msgCmd = 'Registry'
        if msgCmd == 'start':
            msgCmd = 'StartFirst'
        menuReply, title, selMenu = menu.getMenu(msgCmd, msg, userInfo)
        return menuReply, title, msgCmd

    def findNextMenu(menu, findMsg, current_menu, msg: types.Message, userInfo):
        # allMenu = menu.parsed_object['menus']
        allMenu = menu.getMenuReal(msg, userInfo)
        for mm in allMenu:
            id = mm['id']
            if id.lower() == current_menu.lower():
                for itemMenu in mm['menu']:
                    if itemMenu['name'].lower() == findMsg.lower():
                        return itemMenu
        return  None

    async def doStartReview(menu, urlUser, userInfo, msg: types.Message):
        userInfo.urlUser = urlUser
        user = HHresume.proceessResume(urlUser)
        if user is None:
            info = 'Это не резюме'
            await msg.answer(info)
            return
        userInfo.testedUserName = user[0] if user[0] is not None else "Неизвестный"
        userInfo.testedUserWorks = user[1] if user[1] is not None else "Неуказана"
        userInfo.testedUserAnswers = ""
        userInfo.testedUserMode = ""
        userInfo.testedUserQuestId = -1
        
        
        # начало опросы здесь мы после выбора соискателя
        info = 'РЕЗЮМЕ: ' + urlUser
        await msg.answer(info)
        
        msgUser = HHreport.infoUser(user)
        await msg.answer(msgUser)
        # '''
        # формирование списка для опроса по пунктам чертнавыков
        # userInfo.testedUserQuestId = 0
        # skills = HHreport.extractSkill(userInfo)
        # skill = skills[userInfo.testedUserQuestId]
        # msgMenu = f"Вы в режиме собеседования по вашему навыку: <{skill}> \nВы хотите пройти проверку по нему?"   
        # await kbs.gotoMenu(msg, menu, 'menuSelectUser', userInfo, msgMenu)
        
        # '''
        await kbs.startSkillReview(menu, msg,userInfo)
        
        gigaChat = menu.getGigaChat()
        gigaChat.prepare()
        
        # await kbs.doRequest(menu, msg, userInfo)

        userInfo.save()
        return
    # начало опроса по новому навыку
    async def startSkillReview(menu, msg: types.Message, userInfo):
        # userInfo, isNew = kbs.getMainUserInfo(msg)
        skills = HHreport.extractSkill(userInfo)
        if userInfo.testedUserQuestId < 0:
            userInfo.testedUserQuestId = 0
        else:
            userInfo.testedUserQuestId +=1
        userInfo.save()
        # собеседование завершено
        if userInfo.testedUserQuestId >= len(skills):
            return True
        skill = skills[userInfo.testedUserQuestId]
        msgMenu = f"Вы в режиме собеседования по вашему навыку: <{skill}> \nВы хотите пройти проверку по нему?"   
        await kbs.gotoMenu(msg, menu, 'menuSelectUser', userInfo, msgMenu)
        return False
    
    async def get_next_kb(menu, msg: types.Message, bot) -> ReplyKeyboardMarkup:
        userInfo, isNew = kbs.getMainUserInfo(msg)
        
        current_menu = userInfo.current_menu.lower()
        # режим начала опроса
        # if current_menu == 'StartFirst'.lower():
        #     if current_menu == 'setContinue'.lower():
        #         return
        #     # режим пропуска навыка
        #     if current_menu == 'setSkip'.lower():
        #         kbs.startSkillReview(menu, msg)
        #         return
        
        # переход к следующему меню
        next_menu = kbs.findNextMenu(menu, msg.text, current_menu, msg, userInfo)
        if next_menu is not None:
            if 'next' in next_menu:
                msgNext = next_menu['next']
                if 'msg' in next_menu:
                    msgReply = menu.getAssisitans("base", next_menu['msg'], userInfo.assistant)
                    await msg.answer(msgReply)
                    
                menuReply, title, selMenu = menu.getMenu(msgNext, msg, userInfo)
                
                # режим начала опроса
                if next_menu['next'].lower() == 'setContinue'.lower():
                    return
                # режим пропуска навыка
                if next_menu['next'].lower() == 'setSkip'.lower():
                    finesSkills = await kbs.startSkillReview(menu, msg, userInfo)
                    if finesSkills:
                        await msg.answer("Собеседование завршено")
                        await msg.answer("Ваш грейд")
                        await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
                        
                    return
                    
                # режим выбор соискателя
                if current_menu == 'StartFirst'.lower():
                    if 'info' in next_menu:
                        urlUser = next_menu['info']
                        await kbs.doStartReview(menu, urlUser, userInfo, msg)
                        return
                # отладка (завершение общего опроса)
                if next_menu['next'].lower() == 'setFinishCommon'.lower():
                    gigaChat = menu.getGigaChat()
                    await msg.answer('Достаточно. Переходим к техническому опросу')
                    msgReply,indexKey, msgAnswer, LevelMsg, BadLevelMsg =gigaChat.finishCommon()
                    # первый технический вопрос
                    userInfo.testedUserAnswers = userInfo.testedUserAnswers + 'mode:q'  + msgReply
                    userInfo.save()
                    await msg.answer(msgReply)
                    return

                # формирование отчета
                if next_menu['next'].lower() == 'setReport'.lower():
                    # msg = text(bold('Я могу ответить на следующие команды:'),'/voice', '/photo', '/group', '/note', '/file, /testpre', sep='\n')
                    # await msg.reply(msg, parse_mode=ParseMode.MARKDOWN)                    
                    
                    # message = "<font color='red'>Это сообщение с красным текстом!</font>"
                    # await msg.send_message(message)
                    
                    # message_text = text(bold('\nЯ просто напомню,'), 'что есть', code('команда'), '/help')
                    # await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

                    # message = "<b>Это сообщение с красным текстом!</b>"
                    # await msg.answer(message, parse_mode="HTML")

                    gigaChat = menu.getGigaChat()
                    msgReply = await HHreport.infoReport(userInfo, menu, gigaChat, msg)
                    await msg.answer(msgReply)
                    # await msg.answer(msgReply, parse_mode="HTML")
                    return

                # заврешение собеседования
                if next_menu['next'].lower() == 'StartFirst'.lower():
                    # msgReply = menu.getAssisitans("base", 'answer3', userInfo.assistant)
                    msgReply = 'Собеседование завершено'
                    await msg.answer(msgReply)
                    await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
                    return

                # переход в режим собеседованичя
                if next_menu['next'].lower() == 'setTech'.lower():
                    await kbs.doRequest(menu, msg, userInfo)
                    return

            return
        # отрабатываем ввод данных
        else:
            await kbs.getUserData(menu, current_menu, msg, userInfo)

    async def doRequest(menu, msg: types.Message, userInfo):
        testedUserWorks = userInfo.testedUserWorks
        gigaChat = menu.getGigaChat()
        keyAdded = gigaChat.testKey(testedUserWorks)
        if len(keyAdded)==0:
            await msg.answer("Для тестирования нет необходимых навыков")
            return

        msgReply,indexKey, msgAnswer, LevelMsg, BadLevelMsg =gigaChat.requestStep(keyAdded, msg.text)

        userInfo.testedUserMode = 'tech Python'
        if msgReply is None:
            return

        # технический вопрос
        userInfo.testedUserAnswers = userInfo.testedUserAnswers + 'mode:q'  + msgReply
        userInfo.save()

        await msg.answer(msgReply)
        if msgAnswer is not None:
            await msg.answer(msgAnswer)
        if LevelMsg is not None:
            await msg.answer(LevelMsg)
        if BadLevelMsg is not None:
            await msg.answer(BadLevelMsg)
        return
        
    async def showAppParameters(selMenu, msg: types.Message, bot):
        if selMenu is not None:
            video = None
            dir_path = os.path.dirname(os.path.realpath(__file__))
            if 'video' in selMenu:
                video = selMenu['video']
                fileVideo = dir_path + mainConst.DIR_RESOURCE + video
                await bot.send_video(msg.chat.id, open(fileVideo, 'rb'))
            if 'photo' in selMenu:
                photo = selMenu['photo']
                filePhoto = dir_path + mainConst.DIR_RESOURCE + photo
                photo = InputFile(filePhoto)
                await bot.send_photo(msg.chat.id, photo = photo)
                # await bot.send_photo(msg.chat.id, open(filePhoto, 'rb'))
            if 'url' in selMenu:
                url = selMenu['url']
                await msg.reply(f"URL: {url}\n")                
                # await msg.reply(f"URL: {html.quote(url)}\n")                
        return

    async def get_kb_by_idmenu(menu, msg: types.Message, msgCmd) -> ReplyKeyboardMarkup:
        userInfo, isNew = kbs.getMainUserInfo(msg)
        menuReply, title, selMenu = menu.getMenu(msgCmd, msg, userInfo)

        if menuReply is not None:
            userInfo.current_menu = msgCmd
            userInfo.save()
            await msg.answer(title, reply_markup=menuReply)
        else:
            await msg.answer(f"ОШИБКА: меню {msgCmd} не найдено")

    async def setInfoMode(msg: types.Message):
        userInfo, isNew = kbs.getMainUserInfo(msg)
        if isNew == False:
            pieces = msg.text.split()
            if len(pieces)==2:
                mode = pieces[1]
                if mode.isdigit():
                    userInfo.infoMode = int(mode)
                    userInfo.save()
            else:
               await msg.answer("Небходим номер запроса")
        return

    async def setParam(msg: types.Message):
        userInfo, isNew = kbs.getMainUserInfo(msg)
        if isNew == False:
            pieces = msg.text.split()
            if len(pieces)==3:
                all_variables = dir(userInfo)
                paramName = pieces[1]
                for param in all_variables:
                    if param == paramName:
                        value = pieces[2]
                        await msg.answer(f"Параметр {paramName} изменен на {value}")
                        exec(f"userInfo.{paramName} = userType.{value}")
                        paramName = value
                        userInfo.save()
                        return
                await msg.answer("Параметр не нрайден")
            else:
               await msg.answer("Небходим номер запроса")
        return
    def getMainUserInfo(msg: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(msg)
        return userInfo, isNew

    # отработка введенных данных
    async def getUserData(menu, current_menu, msg: types.Message, userInfo):
        # ввод url резюме HH
        if current_menu == "StartFirst".lower():
            urlUser = msg.text
            await kbs.doStartReview(menu, urlUser, userInfo, msg)
            return
        # ввод ответа на вопрос
        if current_menu == "menuSelectUser".lower():
            # testedUserMode = userInfo.testedUserMode + 'einf'
            # userInfo.testedUserAnswers = userInfo.testedUserAnswers + 'mode:' + testedUserMode + msg.text + '\n'
            userMsg = msg.text
            if len(userMsg)>=1:
                if userMsg[0]=='?':
                    gigaChat = menu.getGigaChat()
                    request = msg.text[1:]
                    # уточнение технический вопрос
                    userInfo.testedUserAnswers = userInfo.testedUserAnswers + 'mode:u'  + request
                    msgReply,indexKey, msgAnswer, LevelMsg, BadLevelMsg =gigaChat.nextTech(request)
                    userInfo.testedUserAnswers = userInfo.testedUserAnswers + 'mode:t'  + msgReply
                    userInfo.save()
                    await msg.answer(msgReply)
                else:
                    userInfo.testedUserAnswers = userInfo.testedUserAnswers + 'mode:a'  + msg.text + '\n'
                    userInfo.save()
                    await kbs.doRequest(menu, msg, userInfo)
            return

        await msg.answer("Непонятно")
        return
    
    async def sendMediaData(menu, msg: types.Message):
        userInfo, isNew = kbs.getMainUserInfo(msg)
        current_menu = userInfo.current_menu.lower()
        # сохранение данных для передачи
        if current_menu == "menuConfirmDelivery".lower():
            await kbs.gotoMenu(msg, menu, 'menuCorrespondsToAct', userInfo)
            return True
        # проверка qr кода плоттера для анализа его адреса
        if current_menu == "SelectPlotterByQRMenu".lower():
            InvetoryId = await managerQR.getQr(msg, userInfo)
            if InvetoryId is None:
                await msg.answer("Не QR код. Повторите ввод")
            else:
                await kbs.doEquipmentByInvetoryId(menu, current_menu, msg, userInfo, InvetoryId)
            return True

        return False
    # создание меню с списком заявок
    async def createRequestList(menu, current_menu, msg: types.Message, userInfo, msgNext):
        # if msgNext.lower()=='menuEditRequests'.lower():
        #     requsts = okDesk.getListReqwests(userInfo.okDeskUserId)
        #     return requsts
        return None
    # переход на меню по имени
    async def gotoMenu(msg: types.Message, menu, menuName, userInfo, titleExt = None):
        msgNext = menuName
        menuReply, title, selMenu = menu.getMenu(msgNext, msg, userInfo)

        if menuReply is not None:
            userInfo.current_menu = msgNext
            userInfo.save()
            if titleExt is not None:
                title = titleExt
            await msg.answer(title, reply_markup=menuReply)
    