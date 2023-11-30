import random
from langchain.chat_models import GigaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.prompts import load_prompt
from langchain.chains import LLMChain

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from gigachat.models import Chat, Messages, MessagesRole

# Авторизация в сервисе GigaChat
andyCred = "MTI3YzYzN2ItOGIwOC00NDNiLWJmOGItOGM3N2NmNTYxMjZhOjVjYWYxMjljLWJlMjEtNDQ4Yi05M2Q5LTI1N2ZhMmEzMmU2Mw=="
keyWorlds = [["Python","0"],["Java","1"],["PHP","2"],["C++","3"]]

class gigaChatProcessorOld:
    def __init__(self):
        self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False, temperature=1)
        self.counter = 0
        return
    def testKey(self, testedUserWorks):
        keyAdded = []
        for key in keyWorlds:
            if key[0].lower() in testedUserWorks.lower():
                keyAdded.append(key)
                
        return keyAdded
   
    def start1(self, keyAdded):
        lenKey = len(keyAdded)
        indexKey = random.randint(0,lenKey-1)
        roleReq = MessagesRole.ASSISTANT
        roleReq = MessagesRole.USER
        roleReq = MessagesRole.SYSTEM
        prefReq =""
# 1
        # template = "Ты полезный ассистент, который умеет переводить {input_language} на {output_language}."
        # system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        # human_template = "{text}"
        # human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # chat_prompt = ChatPromptTemplate.from_messages(
        #     [system_message_prompt, human_message_prompt]
        # )

        # # get a chat completion from the formatted messages
        # zz= self.chatAndy(
        #     chat_prompt.format_prompt(
        #         input_language="английский",
        #         output_language="русский",
        #         text="Translate this sentense. I love programming.",
        #     ).to_messages()
        # )
        # print(zz.content)

        
# 2
        messagesBadAsk = [
            SystemMessage(
                content="Ты работодатель, который ищет ведущего программиста. Ты задаешь соискателю вопросы"
            ),
            HumanMessage(content="Придумай соискателю задачу на Yii2. Я опытный программист на Python"),
        ]
        BadAskMsg= self.chatAndy(messagesBadAsk)
        print("\n"+"Неправильный вопрос\n"+BadAskMsg.content)

        messagesAsk = [
            SystemMessage(
                # max_tokens = 10,
                content="Ты работодатель, который ищет ведущего программиста. Ты задаешь соискателю вопросы"
                # content="Ты работодатель, который ищет ведущего программиста на Python. Ты задаешь соискателю вопросы"
                # content="Ты полезный ассистент, который умеет переводить русский на английский."
            ),
            # HumanMessage(content="Придумай соискателю задачу на Yii2. Я опытный программист на Python"),
            # HumanMessage(content="Придумай соискателю сложную вопрос на OpenGL. Я опытный программист"),
            HumanMessage(content="Придумай соискателю сложную задачу на Python. Я опытный программист на Python"),
            # HumanMessage(content="Придумай соискателю сложную задачу на Python + Yii2. Я опытный программист на Python"),
            # HumanMessage(content="Переведи это предложение. Я люблю программирование."),
        ]
        AskMsg= self.chatAndy(messagesAsk)
        print("\n"+"\n"+AskMsg.content)

        messagesAnswer = [
            SystemMessage(
                # content="Ты программист на Python"  
                # n = 2,
                # repetition_penalty = 1,
                # top_p = 1,
                content="Ты программист"
            ),
            HumanMessage(content="Реши эту задачу на Python"+AskMsg.content, example=True),
            # HumanMessage(content="Ответь на этот вопрос OpenGL"+zz.content, example=True),
        ]
        AnswerMsg= self.chatAndy(messagesAnswer)
        print("\n"+"\nРЕШЕНИЕ\n"+AnswerMsg.content)

        messagesLevel = [
            SystemMessage(
                content="Ты программист"
            ),
            # HumanMessage(content="Это правильный ответ:\n"+BadAskMsg.content+"\n на вопрос:\n"+AnswerMsg.content + "?"),
            HumanMessage(content="Это правильный ответ:\n"+AskMsg.content+"\n на вопрос:\n"+AnswerMsg.content + "?"),
        ]
        LevelMsg= self.chatAndy(messagesLevel)
        print("\n"+"\nОценка правльного ответа:\n"+LevelMsg.content)

        messagesBadLevel = [
            SystemMessage(
                content="Ты программист"
            ),
            HumanMessage(content="Это правильный ответ:\n"+BadAskMsg.content+"\n на вопрос:\n"+AnswerMsg.content + "?"),
        ]
        BadLevelMsg= self.chatAndy(messagesBadLevel)
        print("\n"+"\nОценка неправльного ответа\n"+BadLevelMsg.content)

        return prefReq + AskMsg.content, indexKey, AnswerMsg.content , LevelMsg.content, BadLevelMsg.content

        # xx= AIMessage(content='I love programming.', additional_kwargs={}, example=False)
# 3

        msg = keyAdded[indexKey]
        prefReq = f"[{msg[0]}] "
        msgReq = f"Ты рекрутер. Напише мне задачу на Python для кандидата на должность программиста. Сразу напиши правильные ответ"

        messages = [
            SystemMessage(
                role = roleReq,
                # temperature = 2,
                content=msgReq
            )
        ]
        
        # messages = [
        #     AssistantMessage(
        #         # temperature = 2,
        #         HumanMessage(content="Hi, how are you?"),
        #         AIMessage(content="Good, how are you?")
        #         # content=msgReq
        #     )
        # ]
        # messages = [
        #     HumanMessage(content="Hi, how are you?"),
        #     AIMessage(content="Good, how are you?"),
        # ]
        # get_buffer_string(messages)
        res =self.chatAndy(messages)
        messages.append(res)
        
        self.counter += 1
        outStr = res.content
        
        print(outStr)
        
        indexStart = outStr.find(":")
        if indexStart > 0:
            outStr = outStr[indexStart+3:]
        return prefReq + outStr, indexKey
        
        
    def gptRequstVer1(self, roleReuest, requestMsg):
        messages = [
            SystemMessage(
                # role = MessagesRole.USER,
                role = roleReuest,
                # temperature = 2,
                # content="придумать сложный вопрос по Python с примером"
                # content="Напиши 3 вопроса для senior Python"
                # content="Ты рекрутер по senior Python. Напиши 3 вопроса"
                # content="Напиши 5 вопросов по Python"
                # content="Ты рекрутер Напиши 3 вопроса"
                # content="Составить вопросы senior-java"
                # content="что такое def в python"
                content=requestMsg
            )
        ]
        res =self.chatAndy(messages)
        # messages.append(res)
        # self.counter += 1
        return res.content         
        
    def gptRequst(self, contentSystem, contentHuman, printMsg):
        messages = [
            SystemMessage(
                content=contentSystem
            ),
            HumanMessage(content=contentHuman),
        ]
        Msg= self.chatAndy(messages)
        print("\n" + printMsg + "\n"+Msg.content)
        return Msg.content

    def doFullGptRequstVer0(self, key):
        AskMsg = "Вопрос"
        RightAnswerMsg = "Правильный ответ на вопрос"
        LevelMsg = "Ответ на вопрос"
        BadLevelMsg = "Неправильный ответ на вопрос"

        #1 создание неправильного вопроса для проверки
        contentSystem = "Ты работодатель, который ищет ведущего программиста. Ты задаешь соискателю вопросы"
        contentHuman = "Придумай соискателю задачу на Yii2. Я опытный программист на Python"
        BadAskMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "Неправильный вопрос")

        #2 создание правильного вопроса
        contentHuman = "Придумай соискателю сложную задачу на Python. Я опытный программист на Python"
        AskMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "Правильный вопрос")

        #3 получение ответа на правильный вопрос
        contentSystem = "Ты опытный программист. Проверь правильность решения"
        contentHuman = "Реши эту задачу на Python:\n" + AskMsg
        RightAnswerMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "Решение")

        #4 оценка результата на правильный вопрос
        contentHuman = "Вопрос. Это правильный ответ:\n" + AskMsg + "\n на вопрос:\n" + RightAnswerMsg + "?"
        LevelMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "Оценка правльного ответа")

        #5 оценка результата на не правильный вопрос
        contentHuman = "Вопрос. Это правильный ответ:\n" + RightAnswerMsg + "\n на вопрос:\n" +  BadAskMsg + "?"
        # contentHuman = "Вопрос. Это правильный ответ:\n" + BadAskMsg + "\n на вопрос:\n" + RightAnswerMsg + "?"
        print("\nandy\n"+contentHuman+"\n")
        BadLevelMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "Оценка не правльного ответа")
        
        return AskMsg, RightAnswerMsg , LevelMsg, BadLevelMsg

    def doFullGptRequstVer1(self, key):
        AskMsg = "Вопрос"
        RightAnswerMsg = "Правильный ответ на вопрос"
        LevelMsg = "Ответ на вопрос"

        # synonyms_with_examples = load_prompt('lc://prompts/synonyms/synonyms_generation_with_examples.yaml')
        # text = prompt.format(dataset_size_min=5,
        #                         dataset_size_max=10,
        #                         subject="кошка",
        #                         examples='["кот", "котёнок"]')
        
        role = MessagesRole.ASSISTANT
        inf0 = gigaChatProcessor.gptRequstVer1(self,role, "Придумай задачу к собеседованию по Python +sql")
        inf1 = gigaChatProcessor.gptRequstVer1(self,role, "Придумай задачу к собеседованию по Python +sql")
        inf2 = gigaChatProcessor.gptRequstVer1(self,role, "Придумай задачу к собеседованию по Python +sql")
        # inf2 = gigaChatProcessor.gptRequstVer1(self,role, "Задача к собеседованию по Python +sql")
        print("\ninf\n"+inf0+"\n")
        print("\ninf\n"+inf1+"\n")
        print("\ninf\n"+inf2+"\n")
        #2 создание правильного вопроса
        # contentSystem = "Ты опытный программист."
        # 3 Задачи к собеседованию по Python +sql
        contentSystem = "Ты работодатель, который ищет ведущего программиста. Ты задаешь соискателю вопросы с решением задачи"
        contentHuman = "Задача к собеседованию по Python +sql"
        # contentHuman = "Придумай сложную задачу на Python с кодом. Я опытный программист на Python"
        # contentHuman = "Придумай сложную задачу на Python. Я опытный программист на Python"
        # contentHuman = "Придумай соискателю сложную задачу на Python. Я опытный программист на Python"
        AskMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "ВОПРОС\n")

        #3 получение ответа на правильный вопрос
        contentSystem = "Ты опытный программист"
        contentHuman = "Реши эту задачу на Python, без обьяснений:\n" + AskMsg
        contentHuman = AskMsg
        RightAnswerMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "РЕШЕНИЕ\n")

        #4 оценка результата на правильный вопрос
        contentHuman = "Вопрос. Это правильный ответ:\n" + RightAnswerMsg + "\n на вопрос:\n" +  AskMsg + "?"
        # contentHuman = "Вопрос. Это правильный ответ:\n" + AskMsg + "\n на вопрос:\n" + RightAnswerMsg + "?"
        print("\nandy\n"+contentHuman+"\n")
        LevelMsg = gigaChatProcessor.gptRequst(self, contentSystem, contentHuman, "ОЦЕНКА\n")

        return AskMsg, RightAnswerMsg , LevelMsg, None

    def doFullGptRequstVer2(self, key):
        AskMsg = "Вопрос"
        RightAnswerMsg = "Правильный ответ на вопрос"
        LevelMsg = "Ответ на вопрос"

        # synonyms_with_examples = load_prompt('lc://prompts/synonyms/synonyms_generation_with_examples.yaml')
        # text = prompt.format(dataset_size_min=5,
        #                         dataset_size_max=10,
        #                         subject="кошка",
        #                         examples='["кот", "котёнок"]')
        inf1 = None
        inf2 = None
        
        role = MessagesRole.ASSISTANT
        # text ="Придумай задачу к собеседованию по Python +sql"
        text ="Придумай соискателю сложную вопрос по OpenGL. Я опытный программист"
        
        inf0 = gigaChatProcessor.gptRequstVer1(self,role, text)
        # inf1 = gigaChatProcessor.gptRequstVer1(self,role, text)
        # inf2 = gigaChatProcessor.gptRequstVer1(self,role, text)

        return inf0, inf1 , inf2, None

    def start(self, keyAdded):
        lenKey = len(keyAdded)
        indexKey = random.randint(0,lenKey-1)
        prefReq =""
        AskMsg, RightAnswerMsg , LevelMsg, BadLevelMsg = gigaChatProcessor.doFullGptRequstVer2(self, "key");
        return prefReq + AskMsg, indexKey, RightAnswerMsg , LevelMsg, BadLevelMsg
