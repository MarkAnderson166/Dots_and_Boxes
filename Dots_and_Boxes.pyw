# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ----------------------  Dot and Boxes  ---------------------
# ------------------------------------------------------------
# ------------------------------------------------------------

import tkinter as tk
import random
import time

root = tk.Tk()
root.title("Dots_and_Boxes")
boxSize = 60
halfSize = int(boxSize/2)
boardSize = boxSize*11
canvas = tk.Canvas(root, height=boardSize+boxSize, width=boardSize)
canvas.pack()
canvas.configure(bg='dark grey')

gameState = [[[False, False, False, False, False] for i in range(10)] for j in range(10)]
scoreRed  = 0
scoreBlue = 0
turnColor = "red"
difficulty = 70 # percentage chance ai will do the smart thing

# ------------------------------ #
# ------  GUI and basics  ------ #
# ------------------------------ # 

def drawString(textMes):
  canvas.delete("drawString")
  root.update()
  canvas.create_text(5,boardSize+boxSize-3, tag="drawString",
      anchor="sw", font="Times 10", text=textMes)

def drawGUI(): 
  bs = boxSize 
  for i in range (halfSize, boardSize+halfSize, bs):
    for j in range (halfSize, boardSize+halfSize, bs): 
      #canvas.create_line(i, j, boardSize-bs, j, width=3, fill="grey" )
      #canvas.create_line(i, j, i, boardSize-bs, width=3, fill="grey" )   
      canvas.create_oval(i-2, j+2, i+2, j-2, width=6 )
  canvas.create_rectangle( (boardSize/2)-bs*2, boardSize,
                           (boardSize/2)-bs, boardSize+bs,
                           width=2, fill="red")
  canvas.create_rectangle( (boardSize/2)+bs, boardSize,
                           (boardSize/2)+bs*2, boardSize+bs,
                           width=2, fill="blue")

def drawBox(c,r,boxcolor):
  bs = boxSize
  canvas.create_rectangle(halfSize+2+c*bs, halfSize+2+r*bs,
                          bs-1+halfSize+c*bs, bs-1+halfSize+r*bs,
                          width=0, outline=boxcolor, fill=boxcolor)


def lineClickLogic(c,r):
  r, r3, c, c3 = int(r), int(str(r)[2]), int(c), int(str(c)[2])
  if c3 > 2 and c3 < 7 and r3 < 2 and gameState[c][r][1]==0: takeTurn(c,r,1)
  if r3 > 2 and r3 < 7 and c3 > 7 and gameState[c][r][2]==0: takeTurn(c,r,2)
  if c3 > 2 and c3 < 7 and r3 > 7 and gameState[c][r][3]==0: takeTurn(c,r,3)
  if r3 > 2 and r3 < 7 and c3 < 2 and gameState[c][r][4]==0: takeTurn(c,r,4)


def drawLine(c,r,line):
    canvas.delete('highlight')
    x1,y1 = halfSize+c*boxSize, halfSize+r*boxSize
    x2,y2 = halfSize+c*boxSize, halfSize+r*boxSize
    
    if line == 1:
      x2 = x2 + boxSize
      gameState[c][r-1][line+2] = True

    if line == 2:
      x1, x2, y2 = x1 + boxSize, x2 + boxSize, y2 + boxSize
      if c < 9: gameState[c+1][r][line+2] = True

    if line == 3:
      y1, x2, y2 = y1 + boxSize, x2 + boxSize, y2 + boxSize
      if r < 9: gameState[c][r+1][line-2] = True

    if line == 4:
      y2 = y2 + boxSize
      gameState[c-1][r][line-2] = True

    canvas.create_line( x1, y1, x2, y2, width = 5 )
    canvas.create_line( x1, y1, x2, y2, width = 7, fill = 'green', tags='highlight' )
    canvas.create_line( x1, y1, x2, y2, width = 3, fill = 'yellow', tags='highlight' )

    gameState[c][r][line] = True


def updateScore():
  global scoreRed, scoreBlue, turnColor
  canvas.delete("redScore")
  canvas.delete("blueScore")
  canvas.delete("turnMarker")
  root.update()
  
  if turnColor == "red":
    xOffset, start, extent = boxSize*-1, 330, 60
  else:
    xOffset, start, extent = boxSize, 150, 60

  canvas.create_arc( (boardSize/2)+xOffset, boardSize,
                     (boardSize/2), boardSize+boxSize,
                      start = start, extent = extent,
                      width=2, tag="turnMarker", fill="green")
    
  canvas.create_text((boardSize/2)-boxSize*2, boardSize+boxSize,tag="redScore",
                      anchor="sw", font="Times 45", text=scoreRed)
  canvas.create_text((boardSize/2)+boxSize, boardSize+boxSize, tag="blueScore",
                      anchor="sw", font="Times 45", text=scoreBlue)


# ------------------------------- #
# --------- Game Logic ---------- #
# ------------------------------- # 

def takeTurn(c,r,l):
  drawLine(c,r,l)
  if checkAllBoxes():
    autoTurn()
  else:
    global turnColor
    turnColor = "blue"
  updateScore()
  aiTakeTurn()


def checkAllBoxes():
  global scoreRed, scoreBlue
  for i in range(10):
    for j in range(10):
      if sum(gameState[i][j]) == 4:
        gameState[i][j][0] = 1
        if turnColor == "red": scoreRed += 1
        if turnColor == "blue": scoreBlue += 1
        drawBox(i,j,turnColor)
        checkAllBoxes()
        return 1
      

# auto complete for chain wins
def autoTurn():
  for i in range(10):
    for j in range(10):
      if sum(gameState[i][j]) == 3:
        
        for k in range(1,5,1):
          if gameState[i][j][k] == False: drawLine(i,j,k)
        checkAllBoxes()
        root.update()
        root.after(100, autoTurn())


# ------------------------------- #
# ------------- AI -------------- #
# ------------------------------- # 


def aiTakeTurn():

  # -- compile 4 lists of options
  scoringMoves = []
  decentMoves = []
  idiotMoves = []
  randomMoves = []

  for i in range(10):
    for j in range(10):
      if sum(gameState[i][j]) == 3:
        for k in range(1,5,1):
          if gameState[i][j][k] == False:
            scoringMoves.append(str(i)+str(j)+str(k))
      elif sum(gameState[i][j]) == 2:
        for k in range(1,5,1):
          if gameState[i][j][k] == False:
            idiotMoves.append(str(i)+str(j)+str(k))
      elif sum(gameState[i][j]) == 1:
        for k in range(1,5,1):
          if gameState[i][j][k] == False:
            decentMoves.append(str(i)+str(j)+str(k))
      else:
        for k in range(1,5,1):
          if gameState[i][j][k] == False:
            randomMoves.append(str(i)+str(j)+str(k))

  # -- choose move
  global difficulty
  dice = random.randint(1,100)

    # @90 if theres a scoring move avail, ai take it 9/10
  if dice < difficulty and len(scoringMoves):
    choice = random.choice(scoringMoves)
    print('blue making scoring move')

    # @90 if theres no scoring move avail, ai do something really stupid 1/10
  elif dice > difficulty and len(idiotMoves):
    choice = random.choice(idiotMoves)
    print('blue making idiot move')

    # @90 we'll pick a decent over a random 9/10
  elif dice < difficulty and len(decentMoves):
    choice = random.choice(decentMoves)
    print('blue making decent move')

    # if all else fails, pick a random, if random is empty, pick anything
  else:
    if randomMoves:
      choice = random.choice(randomMoves)
    else:
      choice = random.choice(randomMoves+decentMoves+idiotMoves+scoringMoves)
    print('blue making random move')

  # -- take turn
  time.sleep(.4)
  drawLine(int(choice[0]),int(choice[1]),int(choice[2]))
  if checkAllBoxes():
    autoTurn()
  else:
    global turnColor
    turnColor = "red"
  updateScore()



# ------------------------------- #
# ---------- kick-off ----------- #
# ------------------------------- # 

drawGUI()
updateScore()

# ------ mouse input -------

def click(event):
  x, y = (event.x-halfSize)/boxSize, (event.y-halfSize)/boxSize
  if x > 0 and x < 10 and y > 0 and y < 10:
    lineClickLogic(x,y)

root.bind("<Button-1>", click)

root.mainloop()
