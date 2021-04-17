import RPi.GPIO as GPIO 
import serial
import adafruit_thermal_printer
import cups
import os

class Tag():
    def __init__(self, tagName, inner):
        self.tagName = tagName
        self.inner = inner

class Printer():
    def __init__(self):
        uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=3000)
        ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.11)
        self.printer = ThermalPrinter(uart)
        
        self.cupCodes = {
            'fit-to-page' : 'lp -o fit-to-page'
        }

        
        '''
        self.tags = {
            'u_thin' : self.underlineThin(),
            'u_thick' : self.underlineThick(),

            'b' : self.boldOn(),
            
            'strike' : self.strikeOn(),

            'inverse' : self.inverseOn(),
            'upside_down' : self.upsideDownOn(),

            'double_height' : self.doubleHeightOn(),
            'double_width' : self.doubleHeightOff(),

            't1' : self.textSize1(),
            't2' : self.textSize2(),
            't3' : self.textSize3(),

            'justify_L' : self.justifyLeft(),
            'justify_C' : self.justifyCenter(),
            'justify_R' : self.justifyRight()
        }
        self.printer.reset()
        self.printer.set_defaults()
        '''
    def underlineThick(self):
        self.printer.underline = adafruit_thermal_printer.UNDERLINE_THICK

    def underlineThin(self):
        self.printer.underline = adafruit_thermal_printer.UNDERLINE_THIN
    
    def underlineOff(self):
        self.printer.underline = None

    def boldOn(self):
        self.printer.bold = True
    
    def boldOff(self):
        self.printer.bold = False
    
    def strikeOn(self):
        self.printer.strike = True
    
    def strikeOff(self):
        self.printer.strike = False
    
    def inverseOn(self):
        self.printer.inverse = True
    
    def inverseOff(self):
        self.printer.inverse = False

    def upsideDownOn(self):
        self.printer.upside_down = True
    
    def upsideDownOff(self):
        self.printer.upside_down = False

    def doubleHeightOn(self):
        self.printer.double_height = True
    
    def doubleHeightOff(self):
        self.printer.double_height = False
    
    def doubleWidthOn(self):
        self.printer.double_width = True
    
    def doubleWidthOff(self):
        self.printer.double_width = False

    def textSize1(self):
        self.printer.size = adafruit_thermal_printer.SIZE_SMALL
    
    def textSize2(self):
        self.printer.size = adafruit_thermal_printer.SIZE_MEDIUM
    
    def textSize3(self):
        self.printer.size = adafruit_thermal_printer.SIZE_LARGE

    def justifyLeft(self):
        self.printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
    
    def justifyCenter(self):
        self.printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
    
    def justifyRight(self):
        self.printer.justify = adafruit_thermal_printer.JUSTIFY_RIGHT
    
    '''
    #PRINTING MARKDOWN
    def PrintMarkdown(self, text):
        self.tags['u_thick'](self)
        self.printer.print("THICK LINE")
        self.tags['u_thin'](self)
        self.printer.print("THIN LINE")

    def htmlToPhrases(self, text):
        acc = [];
        while(len(text) > 0):

            if text[0] != '<':
                nextOpenTag = text.index('<')
                if nextOpenTag == -1:
                    acc.append(text)
                else:
                    acc.append(text[0:nextOpenTag])
            else:
                acc.append(_getFirstTag(text))
            
            text = text[len(acc[len(acc)  -1]):]
        
        return acc
    
    def _getFirstTag(self, text, acc='', level=0):
        afterOpenChar = text.index('<') +1
        nextTag = text[afterOpenChar]

        if nextTag == '/':
            level += -1
        else:
            level += 1
        
        acc += text[0:afterOpenChar]
        text = text[afterOpenChar:]

        if(level == 0):
            return acc + text[0:text.index('>')+1]
        
        return _getFirstTag(text, acc, level)

    def processLayer(self, layer):
        regex = r'^<(.*)>(.*?)</\1>$'
        regexLayer = re.search(regex, layer)
        tag = Tag(regexLayer.group(1), regexLayer.group(2))
        return tag
    '''

    #PRINTING BITMAP IMAGES
    def PrintBitmap(self, relativePath):
        res = os.system("{command} {path}".format(command=self.cupCodes['fit-to-page'], path=relativePath))
        while(self.GetPrinterStatus() == 4):
            continue

    def PrintBitmaps(self, relativePath):
        res = os.system("lp -o number-up=4 {path}".format(path=relativePath))
        while(self.GetPrinterStatus() == 4):
            continue

    def GetPrinterStatus(self):
        printerName = 'ZJ-58'
        conn = cups.Connection()
        printers = conn.getPrinters()

        for printer in printers.items():
            if printer[0] == printerName:
                printerItems = printer[1]
            return printerItems['printer-state']


    