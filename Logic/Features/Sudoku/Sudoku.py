import Logic.Features.Sudoku.sudokuGen as sk
from Logic.Features.Sudoku.sudokuGen import cell
import Logic.CSVManager as CSVManager
import json
import Logic.MiscFunctions as misc
import datetime
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from Logic.Printer import Printer

class Sudoku():
    def __init__(self, level="Medium"):
        self.level = level
        self.sudoku = {}
        self.hashedSudoku = ""
    
    def GetSudoku(self):
        n = 0

        if self.level == 'Easy':
            p = sk.perfectSudoku()
            solvedPuzzel = []
            for cell in p:
                solvedPuzzel.append(cell.answer)

            s = sk.puzzleGen(p)
            if s[2] != 'Easy':
                return self.GetSudoku()
            
            puzzel = []
            for cell in s[0]:
                puzzel.append(cell.answer)

        if self.level == 'Medium':
            p = sk.perfectSudoku()
            solvedPuzzel = []
            for cell in p:
                solvedPuzzel.append(cell.answer)

            s = sk.puzzleGen(p)

            while s[2] == 'Easy':
                n += 1
                s = sk.puzzleGen(p)
                if n > 50:
                    return self.GetSudoku()

            if s[2] != 'Medium':
                return self.GetSudoku()
            
            puzzel = []
            for cell in s[0]:
                puzzel.append(cell.answer)

        if self.level == 'Hard':
            p = sk.perfectSudoku()
            solvedPuzzel = []
            for cell in p:
                solvedPuzzel.append(cell.answer)

            s = sk.puzzleGen(p)

            while s[2] == 'Easy':
                n += 1
                s = sk.puzzleGen(p)
                if n > 50:
                    return self.GetSudoku()
            
            while s[2] == 'Medium':
                n += 1
                s = sk.puzzleGen(p)
                if n > 50:
                    return self.GetSudoku()

            if s[2] != 'Hard':
                return self.GetSudoku()
            
            puzzel = []
            for cell in s[0]:
                puzzel.append(cell.answer)

        if self.level == 'Insane':
            p = sk.perfectSudoku()
            solvedPuzzel = []
            for cell in p:
                solvedPuzzel.append(cell.answer)

            s = sk.puzzleGen(p)

            while s[2] != 'Insane':
                n += 1
                s = sk.puzzleGen(p)
                if n > 50:
                    return self.GetSudoku()
            
            puzzel = []
            for cell in s[0]:
                puzzel.append(cell.answer)

        self.sudoku = {
            'solved' : solvedPuzzel,
            'unsolved' : puzzel
        }
    
    def SudokuNotRepeated(self):
        name = "Sudoku"
        sudokuString = json.dumps(self.sudoku['solved'])
        self.hashedSudoku = misc.HashString(sudokuString)
        hashedSolution = [
            datetime.datetime.now(),
            self.hashedSudoku
        ]
        
        if CSVManager.VerifyHistoryFile(name):
            if CSVManager.CheckHistoryFile(name, self.hashedSudoku):
                CSVManager.InsertIntoHistoryFile(name, hashedSolution)
                return True
            else:
                while not self.SudokuNotRepeated():
                    self.GetSudoku()
        else:
            columns = ['DATE_TIME', 'VALUE']
            CSVManager.CreateHistoryFile(name, columns)
            CSVManager.InsertIntoHistoryFile(name, hashedSolution)
        
        return True

    def SaveSudoku(self):
        solvedImage = self.CreateSudokuImage(self.sudoku['solved'])
        solvedImage.save("/home/pi/Desktop/Thermal_1.0/Logic/Features/Sudoku/Saved_Sudoku/solved.png")
        unsolvedImage = self.CreateSudokuImage(self.sudoku['unsolved'])
        unsolvedImage.save("/home/pi/Desktop/Thermal_1.0/Logic/Features/Sudoku/Saved_Sudoku/unsolved.png")
        
        #printer = Printer()
        #printer.printer.feed(3)
        #printer.printer.printImage(unsolvedImage)
        #printer.printer.feed(3)

    def SaveSudokuHistory(self):
        data = [
            self.hashedSudoku,
            datetime.datetime.now(),
            "Sudoku",
            json.dumps(self.sudoku)
        ]

        if CSVManager.VerifyQuizFile():
            CSVManager.InsertQuiz(data)
        else:
            CSVManager.CreateQuizFile()
            CSVManager.InsertQuiz(data)

    def PrintSudokuQuestion(self):
        printer = Printer()
        printer.textSize2()
        printer.justifyCenter()
        printer.underlineThick()
        printer.doubleWidthOn()
        printer.doubleHeightOn()
        printer.printer.print("Level: {level}".format(level=self.level))
        printer.printer.feed(1)
        printer.PrintBitmap("/home/pi/Desktop/Thermal_1.0/Logic/Features/Sudoku/Saved_Sudoku/unsolved.png") 	



    def PrintSudokuAnswer(self):
        printer = Printer()
        printer.PrintBitmap("/home/pi/Desktop/Thermal_1.0/Logic/Features/Sudoku/Saved_Sudoku/solved.png")

    def GetSudokuFromHistory(self, sudokuId):
        if CSVManager.VerifyQuizFile():
            self.sudoku = CSVManager.GetQuizItem(sudokuId)
            self.SaveSudoku()

    def GetLatestSudoku(self):
        if CSVManager.VerifyQuizFile():
            self.sudoku = CSVManager.GetLatestSudokuQuiz()
            self.SaveSudoku()
            self.PrintSudokuAnswer()

    def CreateSudokuImage(self, sudoku):
        base = Image.open("/home/pi/Desktop/Thermal_1.0/Logic/Features/Sudoku/Base_Files/baseSuduko.png").convert("RGBA")
        txt = Image.new("RGBA", base.size, (255,255,255,0))
        fnt = ImageFont.truetype("/home/pi/Desktop/Thermal_1.0/Logic/Features/Sudoku/Base_Files/Anton.ttf", 200)
        d = ImageDraw.Draw(txt)
        moveValue = 230

        count = 0
        y = -15

        for i in range(9):
            x = 70
            moveX = 230
            for newI in range(9):
                value = str(sudoku[count])

                if value != "None":
                    d.text((x,y), value, font=fnt, fill=(0,0,0,255))

                count += 1
                x += moveValue
                if newI / 2 == 0:
                    x += 10

            y += moveValue
            if i /2 == 0:
                y += 10
        
        out = Image.alpha_composite(base, txt)

        thresh = 200
        fn = lambda x : 255 if x > thresh else 0
        r = out.convert('L').point(fn, mode='1')

        return r
