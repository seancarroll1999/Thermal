import datetime
from datetime import timedelta
import json
import Logic.CSVManager as CSVManager
import Logic.MiscFunctions as misc

class Riddle:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.riddle = {
            'Question' : question,
            'Answer' : answer
        }
    
    def print(self):
        print(self.question)
        print(self.answer)
    
    def saveQuiz(self):
        data = [
            misc.HashString("{question}{answer}".format(question=self.question, answer=self.answer)),
            datetime.datetime.now(),
            "Riddle",
            json.dumps(self.riddle)
        ]

        if CSVManager.VerifyQuizFile():
            CSVManager.InsertQuiz(data)
        else:
            CSVManager.CreateQuizFile()
            CSVManager.InsertQuiz(data)