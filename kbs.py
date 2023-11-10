import html
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from doHHresume import HHresume
from managerQR import managerQR
from processorMenu import *
from aiogram.types import InputFile
from question import questionProcessor

from report import HHreport

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
        if isNew:
            msgCmd = 'Registry'
        if msgCmd == 'start':
            msgCmd = 'StartFirst'
        menuReply, title, selMenu = menu.getMenu(msgCmd, msg, userInfo)
        return menuReply, title, msgCmd
            
        kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('say 1')
        b2 = KeyboardButton('say 2', request_contact=True)
        b3 = KeyboardButton('say 3')
        kb_clients.add(b1).add(b2).add(b3)
        msgReply = menu.getAssisitans("base", "answer1", 1)
        return kb_clients, 'Test andy'

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
        userInfo.testedUserName = user[0] if not None else "Неизвестный"
        userInfo.testedUserWorks = user[1] if not None else "Неуказана"
        userInfo.testedUserAnswers = ""
        userInfo.testedUserMode = ""
        userInfo.save()
        
        info = 'РЕЗЮМЕ: ' + urlUser
        await msg.answer(info)
        
        msgUser = HHreport.infoUser(user)
        await msg.answer(msgUser)
        
        await kbs.gotoMenu(msg, menu, 'menuSelectUser', userInfo)
        return
    
    async def get_next_kb(menu, msg: types.Message, bot) -> ReplyKeyboardMarkup:
        userInfo, isNew = kbs.getMainUserInfo(msg)
        
        current_menu = userInfo.current_menu.lower()
        # переход к следующему меню
        next_menu = kbs.findNextMenu(menu, msg.text, current_menu, msg, userInfo)
        if next_menu is not None:
            if 'next' in next_menu:
                msgNext = next_menu['next']
                if 'msg' in next_menu:
                    msgReply = menu.getAssisitans("base", next_menu['msg'], userInfo.assistant)
                    await msg.answer(msgReply)
                    
                menuReply, title, selMenu = menu.getMenu(msgNext, msg, userInfo)

                # режим выбор соискателя
                if current_menu == 'StartFirst'.lower():
                    if 'info' in next_menu:
                        urlUser = next_menu['info']
                        await kbs.doStartReview(menu, urlUser, userInfo, msg)
                        return
                # формирование отчета
                if next_menu['next'].lower() == 'setReport'.lower():
                    # msg = text(bold('Я могу ответить на следующие команды:'),'/voice', '/photo', '/group', '/note', '/file, /testpre', sep='\n')
                    # await msg.reply(msg, parse_mode=ParseMode.MARKDOWN)                    
                    
                    # message = "<font color='red'>Это сообщение с красным текстом!</font>"
                    # await msg.send_message(message)

                    msgReply = HHreport.infoReport(userInfo)
                    await msg.answer(msgReply)
                    return

                # заврешение собеседования
                if next_menu['next'].lower() == 'StartFirst'.lower():
                    msgReply = menu.getAssisitans("base", 'answer3', userInfo.assistant)
                    await msg.answer(msgReply)
                    await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
                    return

                # переход в режим общего собеседованичя
                if next_menu['next'].lower() == 'setCommon'.lower():
                    userInfo.testedUserMode = 'common'
                    userInfo.save()
                    msgReply = menu.getAssisitans("base", 'answer4', userInfo.assistant)
                    await msg.answer(msgReply)
                    return

                # переход в режим технического собеседованичя
                if next_menu['next'].lower() == 'setTech'.lower():
                    userInfo.testedUserMode = 'tech Python'
                    userInfo.save()
                    msqQuest = questionProcessor.get_quest(menu)
                    msgReply = menu.getAssisitans("base", 'answer5', userInfo.assistant)
                    await msg.answer(msgReply)
                    return

            return
        # отрабатываем ввод данных
        else:
            await kbs.getUserData(menu, current_menu, msg, userInfo)
        
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
            testedUserMode = userInfo.testedUserMode + 'einf'
            userInfo.testedUserAnswers = userInfo.testedUserAnswers + 'mode:' + testedUserMode + msg.text + '\n'
            userInfo.save()
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
    