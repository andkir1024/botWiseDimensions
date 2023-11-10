import random
class questionProcessor:
    def get_quest(menu):
        quest = menu.parsed_qwest_python
        all = len(quest['answers'] )
        testIndex = random.randrange(0, all)
        return testIndex
    
    def get_quest_byId(menu, index):
        quest = menu.parsed_qwest_python
        msg = quest['answers'][index]['qwest']
        return msg