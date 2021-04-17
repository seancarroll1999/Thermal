from PIL import Image, ImageDraw, ImageFont
from Logic.Printer import Printer

from datetime import datetime
import http.client
import requests

def main():
    base = Image.new("RGBA", (600,201), (50,55,55,30))
    d = ImageDraw.Draw(base)
    d.rectangle((0, 0, 600, 201), fill=(255, 255, 255), outline=(0, 0, 0), width=5)
    d.rectangle((0, 0, 200, 200), fill=(255, 255, 255), outline=(0, 0, 0), width=5)
    fnt = ImageFont.truetype("base/Anton.ttf", 150)
    d.text((25,-10), "17", font=fnt, fill=(0,0,0,255))
    fnt = ImageFont.truetype("base/Anton.ttf", 30)
    d.text((150,39), "th", font=fnt, fill=(0,0,0,255))

    icon = Image.open("base/rain.png").convert("RGBA")
    fnt = ImageFont.truetype("base/Anton.ttf", 30)
    base.paste(icon, (300, 50))

    base.show()
    base.save("TEST_START.png")

class MorningMessage:
    def __init__(self):
        self.value = ""
    
    '''
    def DisplayDate(self):
        base = Image.new("1", (384,384), 1)
        d = ImageDraw.Draw(base)
        #d.rectangle((0, 0, 384, 384), fill=1, outline=0, width=15)
        d.ellipse((0, 0, 150, 200), fill=0, outline=0)
        
        #fnt = ImageFont.truetype("Logic/Features/Morning/base/Anton.ttf", 300)
        #d.text((30,-70), "2", font=fnt, fill=0)

        base.save("Logic/Features/Morning/Test.png")

        x = Printer()
        x.PrintBitmap("Logic/Features/Morning/Test.png")
    '''

    def DisplayDate(self):
        printer = Printer()
        today = datetime.now()

        date = int(today.strftime("%-d"))
        suffix = self.suffix(date)

        printer.justifyCenter()
        printer.doubleHeightOn()
        printer.doubleWidthOn()
        printer.boldOn()
        printer.underlineThick()
        
        printer.printer.print("{day} - {date}{suffix}".format(date=date, suffix=suffix, day=today.strftime("%A")))
        printer.printer.feed(1)

    def suffix(self, i):
        j = i % 10
        k = i % 100

        if(j == 1 and k != 11):
            return "st"

        if(j == 2 and k != 12):
            return "nd"

        if(j == 3 and k != 13):
            return "rd"

        return "th" 
    
    def DisplayTodaysWeather(self):
        printer = Printer()
        '091d27cdf9da20c25b9a9ce63d70d044'
        'api.openweathermap.org/data/2.5/weather?zip=bs57jb,gb&appid=091d27cdf9da20c25b9a9ce63d70d044'
        'connection = http.client.HTTPSConnection(self.HttpsConnection)'

        url = 'https://api.openweathermap.org/data/2.5/onecall?lat=51.462222&lon=-2.542913&exclude=current,minutely,daily&units=metric&appid=091d27cdf9da20c25b9a9ce63d70d044'
        response = requests.get(url)

        currentDT = datetime.now()

        weatherDict = {
            'morning' : [],
            'noon' : [],
            'afternoon' : [],
            'evening' : [],
            'night' : []
        }

        if response.ok:
            jsonHourlyResponse = response.json()['hourly']
            
            for hourlyWeather in jsonHourlyResponse:
                weatherDict = self.ProcessHourlyWeather(hourlyWeather, currentDT, weatherDict)

        for weatherArray in weatherDict:
            weatherDict[weatherArray] = self.ProcessWeatherDictArray(weatherArray, weatherDict[weatherArray])

        print(weatherDict)

        weatherMainTemp = {}

        for weather in weatherDict:
            if weatherDict[weather] != None:
                weatherMain = weatherDict[weather]['weatherMain']

                if weatherMain in weatherMainTemp:
                    weatherMainTemp[weatherMain] = weatherMainTemp[weatherMain]  + 1
                else:
                    weatherMainTemp[weatherMain] = 1
            
        weatherMain = max(weatherMainTemp, key=lambda i: weatherMainTemp[i])
        
        printer.PrintBitmaps("Images/Morning/{weather}.png".format(weather=weatherMain))




    def ProcessWeatherDictArray(self, weatherTitle, weatherArray):
        
        if len(weatherArray) != 0:
            tempSum = 0
            feelsLikeSum = 0

            weatherDict = {}

            for weather in weatherArray:
                tempSum += float(weather['temp'])
                feelsLikeSum += float(weather['feels_like'])
                weatherMain = weather['weather'][0]['main']

                if weatherMain in weatherDict:
                    weatherDict[weatherMain] = weatherDict[weatherMain] + 1
                else:
                    weatherDict[weatherMain] = 1
            
            commonWeather = max(weatherDict, key=lambda i: weatherDict[i])
            averageTemp = round(tempSum / len(weatherArray))
            feelsLikeTemp = round(feelsLikeSum / len(weatherArray))
            return {
                'temp' : averageTemp,
                'feelsLike' : feelsLikeTemp,
                'weatherMain' : commonWeather
            }
            


    

    

    def ProcessHourlyWeather(self, weatherData, currentDT, weatherDict):
        ts = int(weatherData['dt'])
        dt = datetime.utcfromtimestamp(ts)
        
        if currentDT.date() == dt.date():
            print(dt.strftime("%d/%m/%Y, %H:%M:%S"))

            if dt.hour <= 11:
                weatherDict['morning'].append(weatherData)
                return weatherDict
            
            if dt.hour >= 12 and dt.hour < 15:
                weatherDict['noon'].append(weatherData)
                return weatherDict
            
            if dt.hour >= 15 and dt.hour < 18:
                weatherDict['afternoon'].append(weatherData)
                return weatherDict

            if dt.hour >= 17 and dt.hour < 21:
                weatherDict['evening'].append(weatherData)
                return weatherDict

            if dt.hour >= 20:
                weatherDict['night'].append(weatherData)
                return weatherDict

        return weatherDict

'''
>10:00 - morning
11:00-14:00PM - noon
15:00-17:00 - afternoon
17:00-20:00 - evening
20:00-24:00 - night
'''

'''
{
    'dt': 1614546000, 
    'temp': 6.48, 
    'feels_like': 2.89, 
    'pressure': 1033, 
    'humidity': 87, 
    'dew_point': 4.48, 
    'uvi': 0, 'clouds': 0, 
    'visibility': 10000, 
    'wind_speed': 3.37, 
    'wind_deg': 66, 
    'weather': [
        {'id': 800, 
        'main': 'Clear', 
        'description': 'clear sky', 
        'icon': '01n'}
        ], 
    'pop': 0}
'''