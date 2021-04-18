import os.path
import pandas as pd
import json


# region Header File Functions
def VerifyHeaderFile(fileName):
    filePath = GetHeaderFilePath(fileName)
    if os.path.isfile(filePath):
        return True
    return False

def CreateHeaderFile(fileName, columns, data):
    filePath = GetHeaderFilePath(fileName)
    dataFrame = pd.DataFrame(columns = columns)
    dataFrame.loc[-1] = data
    dataFrame.index = dataFrame.index + 1
    dataFrame = dataFrame.sort_index()
    dataFrame.to_csv(filePath, index=False)

def ChangeHeaderRecord(fileName, data):
    filePath = GetHeaderFilePath(fileName)
    dataFrame = pd.read_csv(filePath)
    dataFrame = ReplaceRow(dataFrame, 0, data)
    dataFrame.to_csv(filePath, index=False)

def GetHeaderDetails(fileName):
    filePath = GetHeaderFilePath(fileName)
    dataFrame = pd.read_csv(filePath)
    return dataFrame.loc[0]

def GetHeaderFilePath(fileName):
    return '/home/pi/Desktop/Thermal/Storage/API_Headers/{fileName}.CSV'.format(fileName = fileName)
# endregion

# region History File Functions
def VerifyHistoryFile(fileName):
    filePath = '/home/pi/Desktop/Thermal/Storage/History/{fileName}.CSV'.format(fileName = fileName)
    if os.path.isfile(filePath):
        return True
    return False

def CreateHistoryFile(fileName, columns):
    filePath = CreateHistoryFilePath(fileName)
    dataFrame = pd.DataFrame(columns = columns)
    dataFrame.to_csv(filePath, index=False)

def InsertIntoHistoryFile(fileName, data):
    filePath = CreateHistoryFilePath(fileName)
    dataFrame = pd.read_csv(filePath)
    dataFrame = AddRow(dataFrame, data)
    dataFrame.to_csv(filePath, index=False)

def CheckHistoryFile(fileName, value):
    filePath = CreateHistoryFilePath(fileName)
    dataFrame = pd.read_csv(filePath)
 
    for index, row in dataFrame.iterrows():
        if row.VALUE == value:
            print("duplicate hash found")
            return False

    return True

def CreateHistoryFilePath(fileName):
    return '/home/pi/Desktop/Thermal/Storage/History/{fileName}.CSV'.format(fileName = fileName)
# endregion

# region Quiz History

def VerifyQuizFile():
    filePath = '/home/pi/Desktop/Thermal/Storage/Quiz_History.csv'
    if os.path.isfile(filePath):
        return True
    return False

def CreateQuizFile():
    filePath = '/home/pi/Desktop/Thermal/Storage/Quiz_History.csv'
    columns = ['ID', 'DATETIME', 'TYPE', 'ITEM']
    dataFrame = pd.DataFrame(columns = columns)
    dataFrame.to_csv(filePath, index=False)

def InsertQuiz(data):
    filePath = '/home/pi/Desktop/Thermal/Storage/Quiz_History.csv'
    dataFrame = pd.read_csv(filePath)
    dataFrame = AddRow(dataFrame, data)
    dataFrame.to_csv(filePath, index=False)

def GetQuizItem(id):
    filePath = '/home/pi/Desktop/Thermal/Storage/Quiz_History.csv'
    dataFrame = pd.read_csv(filePath)
    return json.loads(dataFrame.loc[dataFrame['ID'] == id].ITEM.max())

def GetLatestSudokuQuiz():
    filePath = '/home/pi/Desktop/Thermal/Storage/Quiz_History.csv'
    dataFrame = pd.read_csv(filePath)
    return json.loads(dataFrame.loc[(dataFrame['ITEM'] == 'Sudoku').idxmax(),'ITEM'])

# endregion

# region Settings

def VerifySettingsFile():
    filePath = '/home/pi/Desktop/Thermal/Storage/Setting.csv'
    if os.path.isfile(filePath):
        return True
    return False

def CreateSettinsFile():
    filePath = '/home/pi/Desktop/Thermal/Storage/Setting.csv'
    columns = ['NAME', 'VALUE']
    dataFrame = pd.DataFrame(columns = columns)
    dataFrame.to_csv(filePath, index=False)

def InsertSetting(data):
    filePath = '/home/pi/Desktop/Thermal/Storage/Setting.csv'
    dataFrame = pd.read_csv(filePath)
    dataFrame = AddRow(dataFrame, data)
    dataFrame.to_csv(filePath, index=False)

def GetSetting(name):
    filePath = '/home/pi/Desktop/Thermal/Storage/Setting.csv'
    dataFrame = pd.read_csv(filePath)
    return dataFrame.loc[dataFrame['NAME'] == name].ITEM.max()

# endregion

# region TimeEvents

def VerifyTimeFile():
    filePath = '/home/pi/Desktop/Thermal/Storage/Time_Events.csv'
    if os.path.isfile(filePath):
        return True
    return False

def CreateTimeFile():
    filePath = '/home/pi/Desktop/Thermal/Storage/Time_Events.csv'
    columns = ['DATE_TIME', 'EVENT']
    dataFrame = pd.DataFrame(columns = columns)
    dataFrame.to_csv(filePath, index=False)

def InsertTimeEvent(data):
    filePath = '/home/pi/Desktop/Thermal/Storage/Time_Events.csv'
    dataFrame = pd.read_csv(filePath)
    dataFrame = AddRow(dataFrame, data)
    dataFrame.to_csv(filePath, index=False)

def GetTimeEvents():
    filePath = '/home/pi/Desktop/Thermal/Storage/Time_Events.csv'
    dataFrame = pd.read_csv(filePath)
    console.log(dataFrame)

# endregion

# region Row Manipulation
def AddRow(dataFrame, data):
    dataFrame.loc[-1] = data
    dataFrame.index = dataFrame.index + 1
    dataFrame = dataFrame.sort_index()
    return dataFrame

def ReplaceRow(dataFrame, index, data):
    dataFrame.loc[index] = data
    return dataFrame
# endregion


