import random
from langchain.chat_models import GigaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from gigachat.models import Chat, Messages, MessagesRole

# Авторизация в сервисе GigaChat
andyCred = "MTI3YzYzN2ItOGIwOC00NDNiLWJmOGItOGM3N2NmNTYxMjZhOjVjYWYxMjljLWJlMjEtNDQ4Yi05M2Q5LTI1N2ZhMmEzMmU2Mw=="
keyWorlds = [["Python","0"],["Java","1"],["PHP","2"],["C++","3"]]

'''
chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False)

messages = [
    SystemMessage(
        # role = MessagesRole.USER,
        role = MessagesRole.ASSISTANT,
        # temperature = 2,
        # content="придумать сложный вопрос по Python с примером"
        # content="Напиши 3 вопроса для senior Python"
        # content="Ты рекрутер по senior Python. Напиши 3 вопроса"
        # content="Напиши 5 вопросов по Python"
        # content="Ты рекрутер Напиши 3 вопроса"
        content="Составить вопросы senior-java"
    )
]
res = chatAndy(messages)
messages.append(res)
print(res.content)
'''
class gigaChatProcessor:
    def __init__(self):
        self.chatAndy = GigaChat(credentials=andyCred, verify_ssl_certs=False)
        self.counter = 0
        return
    def testKey(self, testedUserWorks):
        keyAdded = []
        for key in keyWorlds:
            if key[0].lower() in testedUserWorks.lower():
                keyAdded.append(key)
                
        return keyAdded
    def start0(self, keyAdded):
        lenKey = len(keyAdded)
        indexKey = random.randint(0,lenKey-1)
        roleReq = MessagesRole.ASSISTANT
        roleReq = MessagesRole.USER
        prefReq =""
        # roleReq = MessagesRole.SYSTEM
        # self.counter = 1
        if self.counter == 0:
            roleReq = MessagesRole.SYSTEM
            msgReq = "Ты рекрутер. начальный  вопрос кандидату"
            indexKey = -1
            prefReq = "[общ.] "
        else:
            msg = keyAdded[indexKey]
            prefReq = f"[{msg[0]}] "
            # msgReq = f"Ты рекрутер. Напише мне вопрос по {msg[0]} кандидату на должность ведущего программиста"
            # msgReq = f"Ты рекрутер. Напише мне задачу на {msg[0]} для кандидата на должность ведущего программиста"
            msgReq = f"Ты рекрутер. Напише мне задачу на {msg[0]} для кандидата на должность программиста"
            # Ты рекрутер.
            # Придумай мне задачу на Python для кандидата на должность программиста
            # Придумай мне вопрос по знанию языка Python 
            # какие вопросы задать python-программисту, чтобы проверить уровень владения Pandas на интервью? Сразу напиши правильные ответы к каждому вопросу 
            # какой один вопрос задать senior python-программисту, чтобы проверить уровень владения  на интервью? Сразу напиши правильные ответ к каждому вопросу
        messages = [
            SystemMessage(
                # role = MessagesRole.USER,
                role = roleReq,
                temperature = 2,
                content=msgReq
            )
        ]
        res =self.chatAndy(messages)
        messages.append(res)
        
        self.counter += 1
        outStr = res.content
        
        print(outStr)
        
        indexStart = outStr.find(":")
        if indexStart > 0:
            outStr = outStr[indexStart+3:]
        return prefReq + outStr, indexKey

    # def testRequest(self,msqTest):
    #     prefReq =""
    #     messages = [
    #         SystemMessage(
    #             role = MessagesRole.USER,
    #             # temperature = 2,
    #             content=msgReq
    #         )
    #     ]
    #     res =self.chatAndy(messages)
    #     messages.append(res)
    #     return res.content


    def start(self, keyAdded):
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
        
