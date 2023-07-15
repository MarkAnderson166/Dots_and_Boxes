# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ----------------------  Dot and Boxes  ---------------------
# ------------------------------------------------------------
# ------------------------------------------------------------

import tkinter as tk
import random

root = tk.Tk()
root.title("Dots_and_Boxes")
boxSize = 60
halfSize = int(boxSize/2)
boardSize = boxSize*11
canvas = tk.Canvas(root, height=boardSize+boxSize, width=boardSize)
canvas.pack()
canvas.configure(bg='grey')

gameState = [[[False, False, False, False, False] for i in range(10)] for j in range(10)]
scoreRed  = 0
scoreBlue = 0
turnColor = "red"

# ------------------------------ #
# ------  GUI and basics  ------ #
# ------------------------------ # 

def drawString(textMes):
  canvas.delete("drawString")
  root.update()
  canvas.create_text(5,boardSize+boxSize-3, tag="drawString",
      anchor="sw", font="Times 10", text=textMes)

def drawDots():  
  for i in range (halfSize, boardSize+halfSize, boxSize):
    for j in range (halfSize, boardSize+halfSize, boxSize): 
      canvas.create_line(i, j, boardSize-boxSize, j, width=3, fill="light grey" )
      canvas.create_line(i, j, i, boardSize-boxSize, width=3, fill="light grey" )   
      canvas.create_oval(i-2, j+2, i+2, j-2, width=6 )

def drawBox(c,r,boxcolor):
  canvas.create_rectangle(halfSize+2+c*boxSize, halfSize+2+r*boxSize, boxSize-1+halfSize+c*boxSize, boxSize-1+halfSize+r*boxSize, width=0,
          outline=boxcolor, fill=boxcolor)

  

def lineClickLogic(c,r):
  r, r3, c, c3 = int(r), int(str(r)[2]), int(c), int(str(c)[2])
  if c3 > 2 and c3 < 7 and r3 < 2 and gameState[c][r][1]==0:
    drawLine(c,r,1)
  if r3 > 2 and r3 < 7 and c3 > 7 and gameState[c][r][2]==0:
    drawLine(c,r,2)
  if c3 > 2 and c3 < 7 and r3 > 7 and gameState[c][r][3]==0:
    drawLine(c,r,3)
  if r3 > 2 and r3 < 7 and c3 < 2 and gameState[c][r][4]==0:
    drawLine(c,r,4)


def drawLine(c,r,line):
    gameState[c][r][line] = True
    if line == 1:
      canvas.create_line(halfSize+c*boxSize, halfSize+r*boxSize,
                         boxSize+halfSize+c*boxSize, halfSize+r*boxSize, width=5 )
      gameState[c][r-1][line+2] = True
    if line == 2:
      canvas.create_line(boxSize+halfSize+c*boxSize, halfSize+r*boxSize,
                         boxSize+halfSize+c*boxSize, boxSize+halfSize+r*boxSize, width=5 )
      if c < 9: gameState[c+1][r][line+2] = True
    if line == 3:
      canvas.create_line(halfSize+c*boxSize, boxSize+halfSize+r*boxSize,
                         boxSize+halfSize+c*boxSize, boxSize+halfSize+r*boxSize, width=5 )
      if r < 9: gameState[c][r+1][line-2] = True
    if line == 4:
      canvas.create_line(halfSize+c*boxSize, halfSize+r*boxSize,
                         halfSize+c*boxSize, boxSize+halfSize+r*boxSize, width=5 )
      gameState[c-1][r][line-2] = True
    checkAllBoxes()
    flipTurn()


def flipTurn():
  global turnColor
  if turnColor == "red":
    turnColor = "blue"
  else:
    turnColor = "red"
  updateScore()


def updateScore():
  global scoreRed
  global scoreBlue
  global turnColor

  canvas.delete("drawRedScore")
  canvas.delete("drawBlueScore")
  canvas.delete("drawRedScoreBox1")
  canvas.delete("drawRedScoreBox2")
  canvas.delete("drawBlueScoreBox1")
  canvas.delete("drawBlueScoreBox2")
  root.update()

  canvas.create_rectangle( 5, boardSize, boxSize, boardSize+boxSize,
                           width=2, tag="drawRedScoreBox1", fill="pink")
  canvas.create_rectangle( 145, boardSize, 145+boxSize, boardSize+boxSize,
                           width=2, tag="drawRedScoreBox1", fill="cyan")
  
  if turnColor == "red":
    canvas.create_rectangle( 5, boardSize, boxSize, boardSize+boxSize,
                           width=2, tag="drawRedScoreBox1", fill="red")
  if turnColor == "blue":
    canvas.create_rectangle( 145, boardSize, 145+boxSize, boardSize+boxSize,
                           width=2, tag="drawRedScoreBox1", fill="blue")
    
  canvas.create_text(15,boardSize+boxSize-3, tag="drawRedScore",
      anchor="sw", font="Times 25", text=scoreRed)
  canvas.create_text(150,boardSize+boxSize-3, tag="drawBlueScore",
      anchor="sw", font="Times 25", text=scoreBlue)


# ------------------------------- #
# --------- Game Logic ---------- #
# ------------------------------- # 

#TODO turns: flip between red and blue

def checkAllBoxes():

  global scoreRed
  global scoreBlue

  for i in range(10):
    for j in range(10):
      if sum(gameState[i][j]) == 4:
        gameState[i][j][0] = 1
        drawBox(i,j,turnColor)
        if turnColor == "red": scoreRed += 1
        if turnColor == "blue": scoreBlue += 1


# ------------------------------- #
# ------------- AI -------------- #
# ------------------------------- # 

#TODO auto complete for chain wins

#TODO make perfect AI, then add probablilties for stupid.

# ------------------------------- #
# ---------- kick-off ----------- #
# ------------------------------- # 

drawDots()
updateScore()

# ------------ mouse input ------------
#def motion(event):
#  x, y = event.x, event.y

def click(event):

  x, y = (event.x-halfSize)/boxSize, (event.y-halfSize)/boxSize
  #drawString('{}, {}'.format(x, y))
  if x > 0 and x < 10 and y > 0 and y < 10:
    lineClickLogic(x,y)

  global turnColor
  print('it is '+turnColor+"'s turn")


#root.bind('<Motion>', motion)
root.bind("<Button-1>", click)

root.mainloop()
