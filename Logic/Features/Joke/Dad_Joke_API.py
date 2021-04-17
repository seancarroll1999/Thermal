from Logic.RapidAPI import RapidApi
import json
import Logic.CSVManager as CSVManager
import datetime
from datetime import timedelta
from Logic.Features.Joke.Joke import Joke

''' 
<SUMMARY>
    -   Creates instances of RapidApi to make calls to Dad-Jokes API
    -   Returns results
    -   Checks for duplicates in HashTable
    -   uses Jokes.py to print joke to ThermalPrinter
</SUMMARY>
'''
class Dad_Joke:
    def __init__(self):
        self.headers = {
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
        }
        self.Name = "Dad_Joke"

    def GetRandomJoke(self):
        api = RapidApi(self.Name, "dad-jokes.p.rapidapi.com", self.headers)
        apiResponse = api.GetResponse("GET", "/random/joke")
        self.ProcessMultipleResponse(apiResponse)
    
    def GetJokeByType(self, type):
        api = RapidApi(self.naNameme, "dad-jokes.p.rapidapi.com", self.headers)
        apiResponse = api.GetResponse("GET", "/joke/type/{type}".format(type=type))
        self.ProcessMultipleResponse(apiResponse)

    def GetJokeById(self, id):
        api = RapidApi(self.Name, "dad-jokes.p.rapidapi.com", self.headers)
        apiResponse = api.GetResponse("GET", "/joke/{id}".format(id=id))
        self.ProcessSingleResponse(apiResponse)
    
    def ProcessSingleResponse(self, apiBody):
        responseContent = json.loads(apiBody)
        responseStatus = responseContent["success"]
        if(responseStatus):
            responseBody = responseContent["body"]
            self.ProcessJoke(responseBody)

    def ProcessMultipleResponse(self, apiBody):
        responseContent = json.loads(apiBody)
        responseStatus = responseContent["success"]
        if(responseStatus):
            jokes = responseContent["body"]

            if len(jokes) == 1:
                self.ProcessJoke(jokes[0])
            else:
                #pick ranodm joke pass through see if there return pick another if there
                print("multiple response not supported")

    def ProcessJoke(self, body):
        saveResponse = [
                datetime.datetime.now(),
                body['_id']
        ]
        if CSVManager.VerifyHistoryFile(self.Name):
            if CSVManager.CheckHistoryFile(self.Name, saveResponse[1]):
                CSVManager.InsertIntoHistoryFile(self.Name, saveResponse)
                self.DisplayJoke(body)
        else:
            columns = ['DATE_TIME', 'VALUE']
            CSVManager.CreateHistoryFile(self.Name, columns)
            CSVManager.InsertIntoHistoryFile(self.Name, saveResponse)
            self.DisplayJoke(body)

    def DisplayJoke(self, responseBody):
        x = Joke(responseBody['setup'], responseBody['punchline'])
        x.print()
