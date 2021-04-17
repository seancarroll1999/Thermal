import http.client
import json
import datetime
from datetime import timedelta

import Logic.CSVManager as CSVManager
import Logic.MiscFunctions as misc
''' 
<SUMMARY>
    -   Base class for Rapid API calls: Rapid API is a common source of calls 
</SUMMARY>
'''
class RapidApi:
    def __init__(self, name, httpsConnection, headers):
        self.Key = '8dc77b31a0msh902fd651db0532cp1c9ad3jsn4e29d936e49c'
        self.Name = name
        self.HttpsConnection = httpsConnection
        self.Headers = headers
        self.Headers['x-rapidapi-key'] = '8dc77b31a0msh902fd651db0532cp1c9ad3jsn4e29d936e49c'
    
    def GetResponse(self, method, request):
        #Makes sure we dont exceed free limit
        if self.ConnectionAvaliable():
            connection = http.client.HTTPSConnection(self.HttpsConnection)
            connection.request(method, request, headers=self.Headers)
            response = connection.getresponse()
            
            #Save Header File
            x = int(response.getheader("X-RateLimit-Free-Plan-Reset") or response.getheader("X-RateLimit-Requests-Reset"))
            headerData = [
                int(response.getheader("X-RateLimit-Free-Plan-Limit") or response.getheader("X-RateLimit-Requests-Limit")),
                int(response.getheader("X-RateLimit-Free-Plan-Remaining") or response.getheader("X-RateLimit-Requests-Remaining")),
                int(response.getheader("X-RateLimit-Free-Plan-Reset") or response.getheader("X-RateLimit-Requests-Reset")),
                datetime.datetime.now() + timedelta(seconds=x)
            ]

            if CSVManager.VerifyHeaderFile(self.Name):
                CSVManager.ChangeHeaderRecord(self.Name, headerData)
            else:
                columns = ['RATE_LIMIT', 'REMAINING', 'SECONDS_UNTIL_REFRESH', 'DATE_REFRESH_AVAILABLE']
                CSVManager.CreateHeaderFile(self.Name, columns, headerData)

            responseString = response.read().decode("utf-8")
            
            return responseString

        else:
            print("limit Exceeded for: {name}".format(name=self.Name))

    def ConnectionAvaliable(self):
        if CSVManager.VerifyHeaderFile(self.Name):
            headerData = CSVManager.GetHeaderDetails(self.Name)
            if headerData.REMAINING -1 > 0:
                return True
            return False
        return True