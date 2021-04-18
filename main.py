import pandas as pd
import Logic.CSVManager as csvM
from Logic.RapidAPI import RapidApi
from Logic.Features.Joke.Dad_Joke_API import Dad_Joke
from Logic.Features.Sudoku.Sudoku import Sudoku
from Logic.Features.Riddle.Riddles_API import Riddles
from Logic.Printer import Printer
from Logic.Features.Morning.Morning import MorningMessage
import adafruit_thermal_printer
import Logic.Button as Button
import time
import threading
import Logic.FunctionCode as Code
from multiprocessing import Process

from flask import Flask , render_template, request, redirect
''' 
<SUMMARY>
    -   Flask implementation for web server for Rest API   
</SUMMARY>
'''

def App():
    #dad_joke = Dad_Joke().GetRandomJoke()

    
    x = Sudoku("Medium")
    x.GetSudoku()
    x.SudokuNotRepeated()
    x.SaveSudoku()
    x.SaveSudokuHistory()
    x.PrintSudokuQuestion()
    x.PrintSudokuAnswer()
    

    #riddle = Riddles().GetRandomRiddle()
    '''
    data = """
    <u><b>Run: </b>Pi</u>
    """
    '''
    #printer = Printer()
    #printer.printer.warm_up(heat_time=127)
    #dprinter.PrintBitmap("Logic/Features/Sudoku/Saved_Sudoku/test.png")
    #printer.printer.print("hello", end="")
    #printer.printer.print("hello", end="")
    #printer.printer.feed(3)

    
    #printer = Printer()
    #printer.PrintMarkdown("<dfd>")
    #printer.printer.feed(2)

    #x = Sudoku()
    #x.GetSudokuFromHistory('c300147405a412f55edd911b0ad1f65b12b318f44b7268ba0b54007e87b6a8f2')
    #x.PrintSudokuQuestion()

app = Flask(__name__)

@app.route('/')
def index():
    return "index"

@app.route('/Sudoku')
def NewSudoku():
    difficulty = request.args.get('difficulty')
    print(difficulty)
    
    if difficulty == 'Easy' or difficulty == 'Medium' or difficulty == 'Hard' or difficulty == 'Insane':
        difficulty = difficulty
    else:
        difficulty = 'Medium'
    
    print("Generating Sudoku...")
    sudoku = Sudoku(difficulty)
    sudoku.GetSudoku()
    sudoku.SudokuNotRepeated()
    sudoku.SaveSudoku()
    sudoku.SaveSudokuHistory()
    print("Printing Sudoku...")
    sudoku.PrintSudokuQuestion()
    
    return "printNew"

@app.route('/AnswerRecentSudoku')
def AnswerRecent():
    #sudoku = Sudoku()
    #sudoku.GetLatestSudoku()
    Code.AnswerRecentSudoku()
    #Button.ShortPress()
    return "printAnswer"

def flaskApp():
    x = Printer()
    x.printer.print("Printer online and ready")
    x.printer.feed(6)
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    proc1 = Process(target=Button.StartButton)
    proc1.start()
    
    proc2 = Process(target=flaskApp)
    proc2.start()
    
    
    #x = Sudoku()
    #x.GetSudokuFromHistory('c300147405a412f55edd911b0ad1f65b12b318f44b7268ba0b54007e87b6a8f2')
    #x.PrintSudokuAnswer()
    #x.PrintSudokuQuestion()
    #x = MorningMessage()
    #x.DisplayDate()
    #x.DisplayTodaysWeather()
    
    

    
