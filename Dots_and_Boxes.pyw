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
boxSize = 50
halfSize = int(boxSize/2)
gridSize = 8
boardSize = boxSize*(gridSize+1)
canvas = tk.Canvas(root, height=boardSize+boxSize, width=boardSize)
canvas.pack()
canvas.configure(bg='dark grey')

gameState = [[[False, False, False, False, False] for i in range(gridSize)] for j in range(gridSize)]
score1 = 0
score2 = 0
colors =['red','green','blue','orange','yellow','purple','pink','cyan']
player1 = random.choice(colors)
colors.remove(player1)
player2 = random.choice(colors)
currentTurn = player1
difficulty = 80 # percentage chance ai will do the smart thing

# ------------------------------ #
# ------  GUI and basics  ------ #
# ------------------------------ # 

def printDebug(str):
  #if 1:
  if 'stupid' in str:
    print(str)

def drawString(textMes):
  canvas.delete("drawString")
  root.update()
  canvas.create_text(5,boardSize+boxSize-3, tag="drawString",
      anchor="sw", font="Times "+str(gridSize), text=textMes)

def drawGUI(): 
  bs = boxSize 
  for i in range (halfSize, boardSize+halfSize, bs):
    for j in range (halfSize, boardSize+halfSize, bs):   
      canvas.create_oval(i-2, j+2, i+2, j-2, width=6 )
  canvas.create_rectangle( (boardSize/2)-bs*3, boardSize,
                           (boardSize/2)-bs, boardSize+bs,
                           width=2, fill=player1)
  canvas.create_rectangle( (boardSize/2)+bs, boardSize,
                           (boardSize/2)+bs*3, boardSize+bs,
                           width=2, fill=player2)

def drawBox(c,r,boxcolor):
  bs = boxSize
  canvas.create_rectangle(halfSize+2+c*bs, halfSize+2+r*bs,
                          bs-1+halfSize+c*bs, bs-1+halfSize+r*bs,
                          width=0, outline=boxcolor, fill=boxcolor)


def lineClickLogic(c,r):
  r, r3, c, c3 = int(r), int(str(r)[2]), int(c), int(str(c)[2])
  if c3 > 1 and c3 < 8 and r3 < 1 and gameState[c][r][1]==0: takeTurn(c,r,1)
  if r3 > 1 and r3 < 8 and c3 > 8 and gameState[c][r][2]==0: takeTurn(c,r,2)
  if c3 > 1 and c3 < 8 and r3 > 8 and gameState[c][r][3]==0: takeTurn(c,r,3)
  if r3 > 1 and r3 < 8 and c3 < 1 and gameState[c][r][4]==0: takeTurn(c,r,4)


def drawLine(c,r,line):
    canvas.delete('highlight')
    x1,y1 = halfSize+c*boxSize, halfSize+r*boxSize
    x2,y2 = halfSize+c*boxSize, halfSize+r*boxSize
    
    if line == 1:
      x2 = x2 + boxSize
      gameState[c][r-1][line+2] = True

    if line == 2:
      x1, x2, y2 = x1 + boxSize, x2 + boxSize, y2 + boxSize
      if c < gridSize-1: gameState[c+1][r][line+2] = True

    if line == 3:
      y1, x2, y2 = y1 + boxSize, x2 + boxSize, y2 + boxSize
      if r < gridSize-1: gameState[c][r+1][line-2] = True

    if line == 4:
      y2 = y2 + boxSize
      gameState[c-1][r][line-2] = True

    canvas.create_line( x1, y1, x2, y2, width = 5 )
    canvas.create_line( x1, y1, x2, y2, width = 7, fill = currentTurn, tags='highlight' )
    canvas.create_line( x1, y1, x2, y2, width = 3, tags='highlight' )

    gameState[c][r][line] = True


def updateScore():
  global score1, score2, currentTurn
  canvas.delete("redScore")
  canvas.delete("blueScore")
  canvas.delete("turnMarker")
  root.update()
  
  #if currentTurn == player1:
  #  xOffset, start, extent = boxSize*-1, 330, 60
  #else:
  #  xOffset, start, extent = boxSize, 150, 60
  #
  #canvas.create_arc( (boardSize/2)+xOffset, boardSize,
  #                   (boardSize/2), boardSize+boxSize,
  #                    start = start, extent = extent,
  #                    width=2, tag="turnMarker", fill="green")
    
  canvas.create_text((boardSize/2)-boxSize*2, boardSize+boxSize,tag="redScore",
                      anchor="sw", font="Times "+str(boxSize-10), text=score1)
  canvas.create_text((boardSize/2)+boxSize, boardSize+boxSize, tag="blueScore",
                      anchor="sw", font="Times "+str(boxSize-10), text=score2)


# ------------------------------- #
# --------- Game Logic ---------- #
# ------------------------------- # 

def takeTurn(c,r,l):
  drawLine(c,r,l)
  if checkAllBoxes():
    autoTurn()
  else:
    global currentTurn
    currentTurn = player2
  updateScore()
  aiTakeTurn()


def checkAllBoxes():
  global score1, score2
  for i in range(gridSize):
    for j in range(gridSize):
      if sum(gameState[i][j]) == 4:
        gameState[i][j][0] = 1
        if currentTurn == player1: score1 += 1
        if currentTurn == player2: score2 += 1
        drawBox(i,j,currentTurn)
        checkAllBoxes()
        return 1
      

# auto complete for chain wins
def autoTurn():
  for i in range(gridSize):
    for j in range(gridSize):
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

  for i in range(gridSize):
    for j in range(gridSize):
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

  #print(idiotMoves,' idiotMoves')
  #print(scoringMoves,' scoringMoves')
  #print(decentMoves,' decentMoves')

  # -- as every move is in our gamestate dataset twice, we need to convert
  # -- the moves in the idiot list to their counterpart then remove them
  for move in idiotMoves:
    move2 = '-blank-'
    if move[2] == '1':
      move2 = move[0]+str(int(move[1])-1)+str(int(move[2])+2)
    if move[2] == '2':
      move2 = str(int(move[0])+1)+move[1]+str(int(move[2])+2)
      #move2 = str(int(move)+102)
    if move[2] == '3':
      move2 = move[0]+str(int(move[1])+1)+str(int(move[2])-2)
      #move2 = str(int(move)+8)
    if move[2] == '4':
      move2 = str(int(move[0])-1)+move[1]+str(int(move[2])-2)
      #move2 = str(int(move)-102)

    printDebug(move+ ' is in idiot list')
    printDebug(move2+' is the same move')

    if move2 in scoringMoves:
      scoringMoves.remove(move2)
    if move2 in decentMoves:
      decentMoves.remove(move2)
    if move2 in randomMoves:
      randomMoves.remove(move2)

  #print(idiotMoves,' idiotMoves')
  #print(scoringMoves,' scoringMoves')
  #print(decentMoves,' decentMoves')


  # -- choose move
  global difficulty
  dice = random.randint(1,100)

    # @90 if theres a scoring move avail, ai take it 9/10
  if dice < difficulty and len(scoringMoves):
    choice = random.choice(scoringMoves)
    printDebug('blue making scoring move')

    # @90 if theres no scoring move avail, ai do something really stupid 1/10
  elif dice > difficulty and len(idiotMoves):
    choice = random.choice(idiotMoves)
    printDebug('blue making a stupid move')

    # @90 we'll pick a decent over a random 9/10
  elif dice < difficulty and len(decentMoves):
    choice = random.choice(decentMoves)
    printDebug('blue making decent move')

    # if all else fails, pick a random, if random is empty, pick anything
  else:
    if randomMoves:
      choice = random.choice(randomMoves)
    else:
      choice = random.choice(randomMoves+decentMoves+idiotMoves+scoringMoves)
    printDebug('player2 making random move')

  # -- take turn
  time.sleep(.4)
  printDebug('player2 making move: '+choice)
  drawLine(int(choice[0]),int(choice[1]),int(choice[2]))
  if checkAllBoxes():
    autoTurn()
  else:
    global currentTurn
    currentTurn = player1
  updateScore()


# ------------------------------- #
# ---------- kick-off ----------- #
# ------------------------------- # 

drawGUI()
updateScore()

# ------ mouse input -------

def click(event):
  x, y = (event.x-halfSize)/boxSize, (event.y-halfSize)/boxSize
  if x > 0 and x < gridSize and y > 0 and y < gridSize:
    lineClickLogic(x,y)

root.bind("<Button-1>", click)

root.mainloop()
