from PIL import Image, ImageDraw, ImageFont

def printSudoku(sudoku, fileName):
    base = Image.open("base/baseSuduko.png").convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))
    fnt = ImageFont.truetype("base/Anton.ttf", 200)
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
    out.save("{fileName}.png".format(fileName=fileName))
    #out.show()