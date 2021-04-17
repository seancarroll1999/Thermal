from Logic.RapidAPI import RapidApi
import json
import Logic.CSVManager as CSVManager
import Logic.MiscFunctions as misc
import datetime
from datetime import timedelta
from Logic.Features.Riddle.Riddle import Riddle

class Riddles:
    def __init__(self):
        self.headers = {
            'x-rapidapi-host': "riddles.p.rapidapi.com"
        }
        self.Name = "Riddles"

    def GetRandomRiddle(self):
        api = RapidApi(self.Name, "riddles.p.rapidapi.com", self.headers)
        apiResponse = api.GetResponse("GET", "/riddle/random")
        self.ProcessResponse(apiResponse)
    
    def ProcessResponse(self, apiBody):
        responseContent = json.loads(apiBody)
        responseAmount = responseContent["success"]["total"]
        if(responseAmount > 0):
            responseBody = responseContent["contents"]

            for riddle in responseBody:
                self.ProcessRiddle(riddle)
    
    def ProcessRiddle(self, riddleBody):
        #Save History
        saveResponse = [
            datetime.datetime.now(),
            riddleBody['id']
        ]

        if CSVManager.VerifyHistoryFile(self.Name):
            if CSVManager.CheckHistoryFile(self.Name, saveResponse[1]):
                CSVManager.InsertIntoHistoryFile(self.Name, saveResponse)
                self.DisplayRiddle(riddleBody)
        else:
            columns = ['DATE_TIME', 'VALUE']
            CSVManager.CreateHistoryFile(self.Name, columns)
            CSVManager.InsertIntoHistoryFile(self.Name, saveResponse)
            self.DisplayRiddle(riddleBody)
        
    
    def DisplayRiddle(self, riddleBody):
        x = Riddle(riddleBody['riddle'], riddleBody['answers'][0])
        x.print()
        x.saveQuiz()