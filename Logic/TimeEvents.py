
import Logic.CSVManager as CSVManager

class TimeEvents:
    def __init__(self):
        self.value = ""
    

    def GetTimeEventsForToday(self):
        if CSVManager.VerifyTimeFile():
            timeEvents = CSVManager.GetTimeEvents()
            print(timeEvents)
        else:
            CSVManager.CreateTimeFile()
    
    def GenerateTodaysRandomEvents(self):
        print("clear current time events")
        print("load from settings the range of time events to produce each day")
        print("generate random events with event_names to print, these can be weighted to produce more of certain type of events")