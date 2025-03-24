from cmu_graphics import *
from PIL import Image, ImageDraw, ImageFont
import math
import random
import time
import os

def onAppStart(app):

    #Importing frames of sprite animations

    app.sprite = 'Dude_Monster.png' 
    app.spriteRunRight = ['Dude_Monster_Run_1.png', 
                     'Dude_Monster_Run_2.png', 
                     'Dude_Monster_Run_3.png', 
                     'Dude_Monster_Run_4.png', 
                     'Dude_Monster_Run_5.png',
                     'Dude_Monster_Run_6.png'] 

    app.spriteRunLeft = ['runFlip1.png', 
                        'runFlip2.png', 
                        'runFlip3.png', 
                        'runFlip4.png', 
                        'runFlip5.png', 
                        'runFlip6.png']
    
    app.spriteJumpRightUp = ['Dude_Monster_Jump_1.png',
                           'Dude_Monster_Jump_2.png',
                           'Dude_Monster_Jump_3.png',
                           'Dude_Monster_Jump_4.png']
    
    app.spriteJumpRightDown = ['Dude_Monster_Jump_5.png',
                                'Dude_Monster_Jump_6.png',
                                'Dude_Monster_Jump_7.png',
                                'Dude_Monster_Jump_8.png']
    
    app.spriteJumpLeftUp = ['Dude_Monster_Jump_1Flip.png',
                          'Dude_Monster_Jump_2Flip.png',
                          'Dude_Monster_Jump_3Flip.png',
                          'Dude_Monster_Jump_4Flip.png']

    app.spriteJumpLeftDown = ['Dude_Monster_Jump_5Flip.png',
                          'Dude_Monster_Jump_6Flip.png',
                          'Dude_Monster_Jump_7Flip.png',
                          'Dude_Monster_Jump_8Flip.png',]
    
            
    app.spriteIdleRight = ['Dude_Monster_Idle_1.png',
                           'Dude_Monster_Idle_2.png',
                           'Dude_Monster_Idle_3.png',
                           'Dude_Monster_Idle_4.png',]
    
    app.spriteIdleLeft = ['Dude_Monster_Idle_1Flip.png',
                          'Dude_Monster_Idle_2Flip.png',
                          'Dude_Monster_Idle_3Flip.png',
                          'Dude_Monster_Idle_4Flip.png',]
    
    app.clouds = ['clouds1.png',
                  'clouds2.png',
                  'clouds3.png',
                  'clouds4.png',
                  'clouds5.png',
                  'clouds6.png',]
    
    app.dustRight = ['dust1.png',
                     'dust2.png',
                     'dust3.png',
                     'dust4.png',]
    
    app.deathRight = ['deathRight1.png',
                      'deathRight2.png',
                      'deathRight3.png',
                      'deathRight4.png',
                      'deathRight5.png']
    
    app.deathLeft = ['deathLeft1.png',
                      'deathLeft2.png',
                      'deathLeft3.png',
                      'deathLeft4.png',
                      'deathLeft5.png',]

    app.isRunning = False   
    app.facingRight = True
    app.runFrame = 0  
    app.runTimer = 0   
    app.runSpeed = 4          

    app.isJumping = False
    app.jumpFrame = 0
    app.jumpTimer = 0
    app.jumpSpeed = 2

    app.idleFrame = 0
    app.idleTimer = 0
    app.idleSpeed = 4

    app.cloudFrame = 0
    app.cloudTimer = 0
    app.cloudSpeed = 4

    app.dustFrame = 0
    app.dustTimer = 0
    app.dustSpeed = 4

    app.dyingFrame = 0
    app.dyingTimer = 80
    app.dyingSpeed = 6

    app.stepDelay = 20
    app.stepsPerSecond = 32
    app.backgroundX = app.width/2 - 161
    app.backgroundY = 20
    app.backgroundWidth = 322
    #app.backgroundColor = rgb(204, 255, 255)
    app.backgroundColor = 'lightBlue'
    app.backgroundHeight = 360
    app.dy = 0
    app.ay = 1.2
    app.timer = 1920
    app.displayTimer = 60
    app.timerBarX = app.width/2 - 161
    app.timerBarY = 386
    app.timerBarHeight = 20

    app.alive = True
    app.dying = False
    app.dieChecker = 1

    app.gems = []

    app.sawblades = []
    app.sawbladesLength = 1
    app.sawbladeColor = 'red'
    app.specialSawblade = None
    makeSawblades(app) 

    app.specialSawblade = []

    app.starAngle = 0

    app.jumps = 0
    app.jumpHoldTime = 0
    app.maxJumpHoldTime = 12
    app.isHoldingJump = False 

    app.widthHalf = 16.5
    app.heightHalf = 21.5

    app.cx = app.width/2
    app.cy = 360 - app.heightHalf
    app.r = 14

    app.umbrellaActive = False
    app.umbrellaCount = 3
    app.umbrellaHalfWidth = 50
    app.umbrellaAngle = 0
    app.umbrellaX = app.cx - app.umbrellaHalfWidth
    app.umbrellaY = app.cy - 75
    app.umbrellaTimer = 320
    app.umbrellaFacingAngle = 0

    app.lineX1 = app.umbrellaX - app.umbrellaHalfWidth + 15
    app.lineY1 = app.umbrellaY
    app.lineX2 = app.umbrellaX + app.umbrellaHalfWidth - 15
    app.lineY2 = app.umbrellaY
    app.canSee = True

    app.score = 0

    app.checker1 = rgb(195, 255, 153)
    app.checker2 = rgb(194, 235, 159)
    app.squareSize = 20
    app.numCols = app.width // app.squareSize
    app.numRows = app.height // app.squareSize 
    app.offsetX = 0
    app.offsetY = 0
    app.fillColor = None

    app.isStarting =True
    app.wordSet1Size = 55
    app.wordSet2Size = 70
    app.wordSet3Size = 45
    app.sizeIncreasing = True
    app.changeSize = 0.1
    app.sawbladesStart = []
    app.transition = False
    app.transitionY = -500
    
def redrawAll(app):

    if app.isStarting == True:
        for row in range(app.numRows + 1):
            for col in range(app.numCols + 1):
                x = col * app.squareSize - app.offsetX % app.squareSize 
                y = row * app.squareSize - app.offsetY % app.squareSize

                effectiveRow = (row + app.offsetY // app.squareSize) % 2 
                effectiveCol = (col + app.offsetX // app.squareSize) % 2

                if (effectiveRow + effectiveCol) % 2 == 0: 
                    drawRect(x, y, app.squareSize, app.squareSize, fill=app.checker1) 
                else: 
                    drawRect(x, y, app.squareSize, app.squareSize, fill=app.checker2)

        for sawblade in app.sawbladesStart:
            drawStar(sawblade.xCoord, sawblade.yCoord, 20, 8, fill='white', border='black', borderWidth=3, rotateAngle=-app.starAngle, roundness=75)
            drawCircle(sawblade.xCoord, sawblade.yCoord, 10, fill= sawblade.color)

        drawRect(0, 0, 400, 500, fill = 'black', opacity = 30)

        drawLabel('Cloudy with', app.width/2, 80 + 5, size=app.wordSet1Size, fill = 'black', bold = True, font='monospace', opacity=60)
        drawLabel('Cloudy with', app.width/2, 80, size=app.wordSet1Size, fill = 'yellow', bold = True, font='monospace', border = 'black')
        drawLabel('a Chance of', app.width/2, 140 + 5, size=app.wordSet1Size, fill = 'black', bold = True, font='monospace', opacity = 60)
        drawLabel('a Chance of', app.width/2, 140, size=app.wordSet1Size, fill = 'yellow', bold = True, font='monospace', border = 'black')
        drawLabel('SAWBLADES', app.width/2, 230 + 5, size=app.wordSet2Size, fill = 'black', bold = True, font='monospace', opacity = 60)
        drawLabel('SAWBLADES', app.width/2, 230, size=app.wordSet2Size, fill = 'red', bold = True, font='monospace', border = 'white')
        drawLabel("Press 'p' to", app.width/2, 300 + 5, size=app.wordSet3Size, fill = 'black', bold = True, font='monospace', opacity = 60)
        drawLabel("Press 'p' to", app.width/2, 300, size=app.wordSet3Size, fill = 'yellow', bold = True, font='monospace', border = 'black')
        drawLabel("Play!", app.width/2, 350 + 5, size=app.wordSet3Size, fill = 'black', bold = True, font='monospace', opacity = 60)
        drawLabel("Play!", app.width/2, 350, size=app.wordSet3Size, fill = 'yellow', bold = True, font='monospace', border = 'black')

        if app.transition:
            drawRect(0, app.transitionY, 400, 500, fill = 'lightCoral')

    elif app.alive:
        for row in range(app.numRows + 1):
            for col in range(app.numCols + 1):
                x = col * app.squareSize - app.offsetX % app.squareSize 
                y = row * app.squareSize - app.offsetY % app.squareSize

                effectiveRow = (row + app.offsetY // app.squareSize) % 2 
                effectiveCol = (col + app.offsetX // app.squareSize) % 2

                if (effectiveRow + effectiveCol) % 2 == 0: 
                    drawRect(x, y, app.squareSize, app.squareSize, fill=app.checker1) 
                else: 
                    drawRect(x, y, app.squareSize, app.squareSize, fill=app.checker2)

        drawRect(app.backgroundX - 4, app.backgroundY - 20, app.backgroundWidth + 8, app.backgroundHeight + 24, fill = 'black', opacity = 70)
        drawRect(app.backgroundX, app.backgroundY - 20, app.backgroundWidth, app.backgroundHeight + 20, fill = app.backgroundColor)
        drawLabel(app.score, app.width/2 + 8, 208, size=130, fill = 'grey', bold = True, font='monospace', opacity=60)
        drawLabel(app.score, app.width/2, 200, size=130, fill = 'red', bold = True, font='monospace', opacity=60, border = 'black')
        drawImage('newGrass.png', app.backgroundX + 1, 357, width = 322 + 2, height = 25)

        drawImage(app.clouds[app.cloudFrame], app.backgroundX, -20, width = 322, height = 250)

        if app.dying:
            if app.facingRight:
                drawImage(app.deathRight[app.dyingFrame], app.cx - 16.5, app.cy - 30, width=40, height=52) 
            else:
                drawImage(app.deathLeft[app.dyingFrame], app.cx - 16.5, app.cy - 30, width=40, height=52) 
                
        elif app.isJumping: 
            if app.facingRight: 
                if app.dy < 0:
                    if app.jumpFrame == 3:
                        drawImage(app.spriteJumpRightUp[app.jumpFrame], app.cx - 16.5, app.cy - 30, width=28, height=43) 
                    else:
                        drawImage(app.spriteJumpRightUp[app.jumpFrame], app.cx - 16.5, app.cy - 30, width=33, height=43) 
                else:
                    drawImage(app.spriteJumpRightDown[app.jumpFrame], app.cx - 16.5, app.cy - 30, width=33, height=43)
            else: 
                if app.dy < 0:
                    if app.jumpFrame == 3:
                        drawImage(app.spriteJumpLeftUp[app.jumpFrame], app.cx - 16.5, app.cy - 30, width=28, height=43) 
                    else:
                        drawImage(app.spriteJumpLeftUp[app.jumpFrame], app.cx - 16.5, app.cy - 30, width=33, height=43) 
                else:
                    drawImage(app.spriteJumpLeftDown[app.jumpFrame], app.cx - 16.5, app.cy - 30, width=33, height=43)
                
        elif app.isRunning:
            if app.facingRight:
                drawImage(app.spriteRunRight[app.runFrame], app.cx - 16.5, app.cy - app.heightHalf, width=33, height=43)
                drawImage(app.dustRight[app.dustFrame], app.cx - 40, app.cy, width = 28, height = 20)
            else:
                drawImage(app.spriteRunLeft[app.runFrame], app.cx - 16.5, app.cy - app.heightHalf, width=33, height=43)
                drawImage(app.dustRight[app.dustFrame], app.cx + 20, app.cy, width = 28, height = 20)
        else: 
            if app.facingRight:
                drawImage(app.spriteIdleRight[app.idleFrame], app.cx - 16.5, app.cy - app.heightHalf, width=29, height=43)
            else:
                drawImage(app.spriteIdleLeft[app.idleFrame], app.cx - 16.5, app.cy - app.heightHalf, width=29, height=43)

        if app.umbrellaActive: 
            drawImage('umbrella.png', app.umbrellaX - app.umbrellaHalfWidth, app.umbrellaY - 50, width=100, height=100, rotateAngle=app.umbrellaAngle)
            drawLine(app.lineX1, app.lineY1, app.lineX2, app.lineY2, rotateAngle=app.umbrellaAngle, fill = 'White')
            #drawCircle(app.cx, app.cy, 55, fill = None, border = 'black')

        for sawblade in app.sawblades:
            drawStar(sawblade.xCoord, sawblade.yCoord, 20, 8, fill='white', border='black', borderWidth=3, rotateAngle=-app.starAngle, roundness=75)
            drawCircle(sawblade.xCoord, sawblade.yCoord, 10, fill= sawblade.color)
        
        for specialSawblade in app.specialSawblade: 
            drawStar(specialSawblade.xCoord, specialSawblade.yCoord, specialSawblade.radius, 8, fill='white', border='black', borderWidth=3, rotateAngle=-app.starAngle, roundness=75) 
            drawCircle(specialSawblade.xCoord, specialSawblade.yCoord, 10, fill=specialSawblade.color)
            if app.canSee:
                drawLine(specialSawblade.xCoord, specialSawblade.yCoord, app.cx, app.cy, fill = 'red', dashes = True, arrowStart=False, arrowEnd=True)
            else:
                drawLine(specialSawblade.xCoord, specialSawblade.yCoord, app.cx, app.cy, fill = 'black', dashes = True, arrowStart=False, arrowEnd=False)

        for gem in app.gems:
            drawCircle(gem.xCoord, gem.yCoord, gem.radius, fill=gem.color, border = 'black')
        
        drawRect(app.timerBarX, app.timerBarY + 5, app.backgroundWidth, app.timerBarHeight, fill = 'lightCoral', border = 'black')
        drawRect(app.timerBarX, app.timerBarY + 5, ((app.displayTimer / 60) * app.backgroundWidth), app.timerBarHeight, fill = 'gold', border = 'black')
        drawLabel(app.displayTimer, app.width/2, 401, size = 18, fill = 'black', bold = True)

        if app.umbrellaCount == 3:
            drawImage('umbrellaNEWEST.png', 50, 397, width=120, height=120, rotateAngle = -35)
            drawImage('umbrellaNEWEST.png', 150, 397, width=120, height=120, rotateAngle = -35)
            drawImage('umbrellaNEWEST.png', 250, 397, width=120, height=120, rotateAngle = -35)

        elif app.umbrellaCount == 2:
            drawImage('umbrellaNEWEST.png', 50, 397, width=120, height=120, rotateAngle = -35)
            drawImage('umbrellaNEWEST.png', 150, 397, width=120, height=120, rotateAngle = -35)
            drawImage('umbrellaNEWEST.png', 250, 397, width=120, height=120, rotateAngle = -35, opacity = 30)

        elif app.umbrellaCount == 1:
            drawImage('umbrellaNEWEST.png', 50, 397, width=120, height=120, rotateAngle = -35)
            drawImage('umbrellaNEWEST.png', 150, 397, width=120, height=120, rotateAngle = -35, opacity = 30)
            drawImage('umbrellaNEWEST.png', 250, 397, width=120, height=120, rotateAngle = -35, opacity = 30)
        
        else: 
            drawImage('umbrellaNEWEST.png', 50, 397, width=120, height=120, rotateAngle = -35, opacity = 30)
            drawImage('umbrellaNEWEST.png', 150, 397, width=120, height=120, rotateAngle = -35, opacity = 30)
            drawImage('umbrellaNEWEST.png', 250, 397, width=120, height=120, rotateAngle = -35, opacity = 30)

        if app.transition:
            drawRect(0, app.transitionY, 400, 500, fill = 'lightCoral')
        
    else:
        for row in range(app.numRows + 1):
            for col in range(app.numCols + 1):
                x = col * app.squareSize - app.offsetX % app.squareSize 
                y = row * app.squareSize - app.offsetY % app.squareSize

                effectiveRow = (row + app.offsetY // app.squareSize) % 2 
                effectiveCol = (col + app.offsetX // app.squareSize) % 2

                if (effectiveRow + effectiveCol) % 2 == 0: 
                    drawRect(x, y, app.squareSize, app.squareSize, fill=app.checker1) 
                else: 
                    drawRect(x, y, app.squareSize, app.squareSize, fill=app.checker2)

        drawLabel('Game', app.width/2, 120, size = 120, fill = 'red', bold = True, font='monospace', opacity=80)
        drawLabel('Over!', app.width/2, 240, size = 120, fill = 'red', bold = True, font='monospace', opacity=80)
        drawLabel(f"Press 'r' to restart", app.width/2, 340, size = 20, fill = 'red', bold = True, font='monospace', opacity=80)

def onKeyPress(app, key):
    if app.isStarting:
        if key == 'p':
            app.transition = True
            if app.transitionY == 0:
                app.isStarting = False

    elif app.alive and not app.dying:
        if key == 'up' and app.jumps < 2:
            app.isJumping = True
            if app.jumps == 0:
                app.isHoldingJump = True
                app.jumpFrame = 0
                app.jumpHoldTime = 0
                app.dy = -5
            elif app.jumps == 1:
                app.dy = -11
                app.jumpFrame = 0
                app.jumps += 1

        if key == 'right':
            if not app.isJumping:
                app.isRunning = True
            app.facingRight = True

        if key == 'left':
            if not app.isJumping:
                app.isRunning = True 
            app.facingRight = False 

        if key == 'w' and app.umbrellaCount > 0: 
            app.umbrellaActive = True 
            app.umbrellaX = app.cx 
            app.umbrellaY = app.cy - 50
            app.umbrellaCount -= 1 
            app.umbrellaAngle = 0
        
        if key == 's' and app.umbrellaActive:
            app.umbrellaActive = False

    else:
        if key == 'r':
            onAppStart(app)

def onKeyRelease(app, key):
    if key == 'up' and app.isHoldingJump:
        app.isHoldingJump = False
        app.jumps += 1

    if (key == 'right' or key == 'left') and not app.isJumping:
        app.isRunning = False
        app.runFrame = 0

def onKeyHold(app, keys):

    if 'right' in keys and not app.isJumping and not app.dying:
        app.cx = min(app.cx + 7, app.backgroundX + app.backgroundWidth - app.widthHalf)
        app.isRunning = True
    elif 'left' in keys and not app.isJumping and not app.dying:
        app.cx = max(app.cx - 7, app.backgroundX + app.widthHalf)
        app.isRunning = True
    
    if 'right' in keys and app.isJumping and not app.dying:
        app.cx = min(app.cx + 7, app.backgroundX + app.backgroundWidth - app.widthHalf)
    elif 'left' in keys and app.isJumping and not app.dying:
        app.cx = max(app.cx - 7, app.backgroundX + app.widthHalf)

    if app.umbrellaActive: 

        if 'a' in keys: 
            app.umbrellaAngle -= 8
        elif 'd' in keys: 
            app.umbrellaAngle += 8
        
def onStep(app):
    app.offsetX += 0.25
    app.offsetY += 0.25

    if app.offsetX >= app.width:
        app.offsetX = 0
    if app.offsetY >= app.height:
        app.offsetY = 0

    if app.isStarting == True:

        if app.sizeIncreasing:
            app.wordSet1Size += app.changeSize
            app.wordSet2Size += app.changeSize
            app.wordSet3Size += app.changeSize
            if app.wordSet1Size >= 56:
                app.sizeIncreasing = False
        
        elif not app.sizeIncreasing:
            app.wordSet1Size -= app.changeSize
            app.wordSet2Size -= app.changeSize
            app.wordSet3Size -= app.changeSize
            if app.wordSet1Size <= 54:
                app.sizeIncreasing = True

        if len(app.sawbladesStart) < 100:
            if random.random() < 0.8:
                makeSawbladesIntro(app)

        for sawblade in app.sawbladesStart:
            bounceHorizontallySawbladeIntro(app, sawblade)
            bounceVerticallySawbladeIntro(app, sawblade)

        app.starAngle -= 20

        if app.transition == True:
            if app.transitionY <= 500:
                app.transitionY += 50
            else:
                app.transition = False

            if app.transitionY >= 0:
                app.isStarting = False

    elif app.dying:
        app.canSee = False
        if app.dieChecker == 1:
            app.dy = 0
            app.dieChecker += 1
        else:   
            app.backgroundColor = 'lightCoral'
            app.dyingTimer -= 1

            app.dy += app.ay / 10
            app.cy -= app.dy

            if app.dyingTimer % 10 == 0:
                if app.dyingFrame < len(app.deathRight) - 1:
                    app.dyingFrame = (app.dyingFrame + 1) 
                else:
                    app.dyingFrame = app.dyingFrame


        if app.dyingTimer <= 0:
            app.alive = False
            app.dying = False
        
    elif app.alive:
        if app.transition == True:
            if app.transitionY <= 500:
                app.transitionY += 30
            else:
                app.transition = False

        if app.isHoldingJump and app.jumps == 0:
            if app.jumpHoldTime < app.maxJumpHoldTime:
                app.jumpHoldTime += 1
                holdFactor = (1 - (app.jumpHoldTime / app.maxJumpHoldTime)) ** 1.65
                app.dy = -6.5 - (6.5 * holdFactor)

        if app.isRunning:
            app.runTimer += 1
            if app.runTimer % app.runSpeed == 0:
                app.runFrame = (app.runFrame + 1) % len(app.spriteRunRight)

            app.dustTimer += 1
            if app.dustTimer % app.dustSpeed == 0:
                app.dustFrame = (app.dustFrame + 1) % len(app.dustRight)
        
        app.cloudTimer += 1
        if app.cloudTimer & app.cloudSpeed == 0:
            app.cloudFrame = (app.cloudFrame + 1) % len(app.clouds)

        if app.isJumping: 
            singleJumpPeak = app.backgroundY + app.heightHalf - app.maxJumpHoldTime * app.ay
            doubleJumpPeak = singleJumpPeak - 11

            heightRatio = 1

            if app.jumps == 0: 
                heightRatio = (app.cy - app.backgroundY) / singleJumpPeak 
            elif app.jumps == 1: 
                heightRatio = (app.cy - app.backgroundY) / doubleJumpPeak

            app.jumpSpeed = max(int(100 / (heightRatio + 0.1)), 1)

            app.jumpTimer += 1 
            if app.jumpTimer % app.jumpSpeed == 0: 
                if app.dy < 0:
                    app.jumpFrame = (app.jumpFrame + 1) % len(app.spriteJumpRightUp)
                    if app.facingRight: 
                        app.currentSprite = app.spriteJumpRightUp[app.jumpFrame] 
                    else: 
                        app.currentSprite = app.spriteJumpLeftUp[app.jumpFrame]

                elif app.dy > 0:
                    app.jumpFrame = (app.jumpFrame + 1) % len(app.spriteJumpRightDown)
                    if app.facingRight: 
                        app.currentSprite = app.spriteJumpRightDown[app.jumpFrame] 
                    else: 
                        app.currentSprite = app.spriteJumpLeftDown[app.jumpFrame]
        
        if app.isRunning == False:
            app.idleTimer += 1
            if app.idleTimer % app.idleSpeed == 0:
                app.idleFrame = (app.idleFrame + 1) % len(app.spriteIdleRight)

        app.dy += app.ay
        app.cy += app.dy 

        if app.cy + app.heightHalf > app.backgroundY + app.backgroundHeight:
            app.cy = app.backgroundY + app.backgroundHeight - app.heightHalf
            app.dy = 0 
            app.jumps = 0
            app.jumpFrame = 0
            app.isJumping = False
            app.isRunning = False

        if app.cy - app.heightHalf < app.backgroundY:
            app.cy = app.backgroundY + app.heightHalf
            app.dy = 0

        for sawblade in app.sawblades:
            bounceHorizontallySawblade(app, sawblade)
            bounceVerticallySawblade(app, sawblade)
        
        if app.score < 2:
            app.sawbladesLength = 1
        elif app.score < 10:
            app.sawbladesLength = 2
        elif app.score < 25:
            app.sawbladesLength = 3
        elif app.score < 45:
            app.sawbladesLength = 4
        else:
            app.sawbladesLength = 5

        if len(app.sawblades) < app.sawbladesLength:
            if random.random() < 0.03:
                makeSawblades(app)
        
        app.starAngle -= 20

        for gem in app.gems:
            gem.dy += app.ay
            gem.yCoord += gem.dy

            gem.xCoord += gem.dx
            gem.dx *= 0.98

            if gem.yCoord + gem.radius > app.backgroundY + app.backgroundHeight:
                gem.yCoord = app.backgroundY + app.backgroundHeight - gem.radius
                gem.dy = -gem.dy * 0.5
                if abs(gem.dy) < 1:
                    gem.dy = 0
                    gem.dx = 0
            
            if gem.xCoord - gem.radius < app.backgroundX:
                gem.xCoord = app.backgroundX + gem.radius
                gem.dx = -gem.dx

            elif gem.xCoord + gem.radius > app.backgroundX + app.backgroundWidth:
                gem.xCoord = app.backgroundX + app.backgroundWidth - gem.radius
                gem.dx = -gem.dx

        app.timer -= 1
        app.displayTimer = math.ceil(app.timer/32)

        if app.umbrellaActive: 
            distanceToPlayer = 30
            angleRadians = math.radians(app.umbrellaAngle) + (math.pi / 2)
            app.umbrellaX = app.cx + distanceToPlayer * (-math.cos(angleRadians))
            app.umbrellaY = app.cy - distanceToPlayer * (math.sin(angleRadians))
            app.lineX1 = app.umbrellaX - app.umbrellaHalfWidth + 15 
            app.lineY1 = app.umbrellaY 
            app.lineX2 = app.umbrellaX + app.umbrellaHalfWidth - 15
            app.lineY2 = app.umbrellaY

            app.umbrellaTimer -= 1
            if app.umbrellaTimer <= 0:
                app.umbrellaActive = False
                app.umbrellaTimer = 320
            #print(f"Umbrella Active: {app.umbrellaActive}")
            #print(f"Umbrella Line: ({app.lineX1}, {app.lineY1}) to ({app.lineX2}, {app.lineY2})")

        for specialSawblade in app.specialSawblade:
            specialSawblade.moveTowardsPlayer(app, app.cx, app.cy)
            #print(f"Sawblade at ({specialSawblade.xCoord}, {specialSawblade.yCoord})")
            #print(f"canSee Result: {canSee(specialSawblade.xCoord, specialSawblade.yCoord, app.cx, app.cy, app.lineX1, app.lineY1, app.lineX2, app.lineY2)}")

        checkPlayerJumpOver(app)
        checkPlayerJumpOverSpecial(app)
        collisionCheckerBlade(app)
        collisionCheckerGem(app)
        checkSpecialSawbladeCollision(app)
        pathTrackingSawbladeMaker(app)
        checkTimer(app)

def checkPlayerJumpOver(app):
    sawbladesToRemove = []
    for sawblade in app.sawblades:
        if app.cy + app.heightHalf < sawblade.yCoord + 20 and abs(app.cx - sawblade.xCoord) <= 20:
            if sawblade.destroyTime is None:
                sawblade.destroyTime = time.time()
            sawblade.color = 'green'

    for sawblade in app.sawblades:
        if sawblade.destroyTime is not None and time.time() - sawblade.destroyTime >= 0.75:
            sawbladesToRemove.append(sawblade)

    for sawblade in sawbladesToRemove:
        app.sawblades.remove(sawblade)
        app.score += 1
        makeGems(app, sawblade.xCoord, sawblade.yCoord)

def checkPlayerJumpOverSpecial(app):
    specialSawbladesToRemove = []
    for specialSawblade in app.specialSawblade:
        if app.cy + app.heightHalf < specialSawblade.yCoord + 20 and abs(app.cx - specialSawblade.xCoord) <= 20:
            if specialSawblade.destroyTime is None:
                specialSawblade.destroyTime = time.time()
            specialSawblade.color = 'green'

    for specialSawblade in app.specialSawblade:
        if specialSawblade.destroyTime is not None and time.time() - specialSawblade.destroyTime >= 0.75:
            specialSawbladesToRemove.append(specialSawblade)

    for specialSawblade in specialSawbladesToRemove:
        app.specialSawblade.remove(specialSawblade)
        app.score += 1
        makeGems(app, specialSawblade.xCoord, specialSawblade.yCoord)
        makeGems(app, specialSawblade.xCoord, specialSawblade.yCoord)
        makeGems(app, specialSawblade.xCoord, specialSawblade.yCoord)
    
def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def checkSpecialSawbladeCollision(app):
    for specialSawblade in app.specialSawblade:
        xLength = abs(app.cx - specialSawblade.xCoord)
        yLength = abs(app.cy - specialSawblade.yCoord)

        if xLength - app.widthHalf < -2 and yLength - app.heightHalf < -2:
            app.dying = True

def collisionCheckerBlade(app):
    for sawblade in app.sawblades:
        xLength = abs(app.cx - sawblade.xCoord)
        yLength = abs(app.cy - sawblade.yCoord)

        if xLength - app.widthHalf < -2 and yLength - app.heightHalf < -2:
            app.dying = True

def collisionCheckerGem(app):
    for gem in app.gems:

        xLength = abs(app.cx - gem.xCoord)
        yLength = abs(app.cy - gem.yCoord)

        if xLength - app.widthHalf < 5 and yLength - app.heightHalf < 5:
            app.gems.remove(gem)
            app.timer += 32

def bounceHorizontallySawblade(app, sawblade):
    sawblade.xCoord += sawblade.sawbladeDX
    if sawblade.xCoord + sawblade.radius >= app.backgroundX + app.backgroundWidth:
        sawblade.xCoord = (app.backgroundX + app.backgroundWidth) - sawblade.radius
        sawblade.sawbladeDX = -sawblade.sawbladeDX
    elif sawblade.xCoord - sawblade.radius <= app.backgroundX:
        sawblade.xCoord = app.backgroundX + sawblade.radius
        sawblade.sawbladeDX = -sawblade.sawbladeDX

def bounceVerticallySawblade(app, sawblade):
    sawblade.yCoord += sawblade.sawbladeDY

    if sawblade.yCoord + sawblade.radius >= app.backgroundY + app.backgroundHeight:
        sawblade.yCoord = (app.backgroundY + app.backgroundHeight) - sawblade.radius
        sawblade.sawbladeDY = -sawblade.sawbladeDY

    for sawblade in app.sawblades:
        if sawblade.yCoord + sawblade.radius + 100 <= 0:
            app.sawblades.remove(sawblade)

def bounceHorizontallySawbladeIntro(app, sawblade):
    sawblade.xCoord += sawblade.sawbladeDX
    if sawblade.xCoord - sawblade.radius >= 403:
        app.sawbladesStart.remove(sawblade)
    elif sawblade.xCoord + sawblade.radius <= -3:
        app.sawbladesStart.remove(sawblade)

def bounceVerticallySawbladeIntro(app, sawblade):
    sawblade.yCoord += sawblade.sawbladeDY
    for sawblade in app.sawbladesStart:
        if sawblade.yCoord - sawblade.radius >= 503:
            app.sawbladesStart.remove(sawblade)

def checkTimer(app):
    if app.displayTimer <= 0:
        app.alive = False

def makeGems(app, sawbladeX, sawbladeY):
    gem = gems(sawbladeX, sawbladeY, 6)
    gem.dy = -15
    gem.dx = random.uniform(-3, 3)
    app.gems.append(gem)

def makeSawblades(app):
    randomX = random.randint(70, 330)
    yCoord = 0
    sawbladeDX = random.choice([random.uniform(-6, -4), random.uniform(4, 6)])
    sawbladeDY = 5
    radius = 20
    sawblade = sawblades(randomX, yCoord, sawbladeDX, sawbladeDY, radius)
    app.sawblades.append(sawblade)

def makeSawbladesIntro(app):
    randomX = random.randint(5, 395)
    yCoord = -5
    sawbladeDX = random.choice([random.uniform(-3, -1), random.uniform(1, 3)])
    sawbladeDY = 5
    radius = 20
    sawblade = sawblades(randomX, yCoord, sawbladeDX, sawbladeDY, radius)
    app.sawbladesStart.append(sawblade)

def pathTrackingSawbladeMaker(app):
    randomNum = random.randint(1, 150)
    if randomNum == 52:
        if app.score >= 5 and len(app.specialSawblade) == 0:
            makeSpecialSawblades(app)

    '''if len(app.specialSawblade) == 0:
        makeSpecialSawblades(app)'''

def makeSpecialSawblades(app):
    randomX = random.randint(70, 330)
    yCoord = 0
    radius = 20
    special = specialSawblade(randomX, yCoord, radius)
    app.specialSawblade.append(special)

def canSee(x1, y1, x2, y2, x3, y3, x4, y4):

    def determinant(a, b, c, d):
        return a * d - b * c
    
    def inBoundingBox(x, y, xMin, xMax, yMin, yMax): 
        return xMin - 1e-6 <= x <= xMax + 1e-6 and yMin - 1e-6 <= y <= yMax + 1e-6

    a1 = y2 - y1
    b1 = x1 - x2 
    c1 = a1 * x1 + b1 * y1

    a2 = y4 - y3 
    b2 = x3 - x4 
    c2 = a2 * x3 + b2 * y3

    det = determinant(a1, b1, a2, b2)
    print(f"Determinant: {det}")

    if det == 0:
        print("Lines are parallel")
        return True
    
    x = (b2 * c1 - b1 * c2) / det 
    y = (a1 * c2 - a2 * c1) / det
    print(f"Intersection Point: ({x}, {y})")

    margin = 0

    inBox1 = inBoundingBox(x, y, min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2))
    inBox2 = inBoundingBox(x, y, min(x3, x4), max(x3, x4), min(y3, y4), max(y3, y4))
    print(f"In Box 1: {inBox1}, In Box 2: {inBox2}")

    if inBox1 and inBox2: 
        print("Intersection is within both bounding boxes") 
        return False 
    return True


class sawblades:
    def __init__(self, xCoord, yCoord, sawbladeDX, sawbladeDY, radius):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.color = 'red'
        self.sawbladeDX = sawbladeDX
        self.sawbladeDY = sawbladeDY
        self.radius = radius
        self.destroyTime = None

class gems:
    def __init__(self, xCoord, yCoord, radius):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.color = 'gold'
        self.radius = radius
        self.dy = 0
        self.dx = 0

class specialSawblade:
    def __init__(self, xCoord, yCoord, radius):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.color = 'gold'
        self.radius = radius
        self.destroyTime = None
        self.speed = 4
        self.direction = None
        self.DX = 0
        self.DY = 0
        self.tracking = True

    def moveTowardsPlayer(self, app, playerX, playerY):
        dx = playerX - self.xCoord
        dy = playerY - self.yCoord
        dist = ((dx)**2 + (dy)**2)**0.5

        if dist != 0:
            if app.umbrellaActive:
                if not canSee(self.xCoord, self.yCoord, playerX, playerY, app.lineX1, app.lineY1, app.lineX2, app.lineY2): 
                    print("Umbrella blocks the line of sight.")
                    app.canSee = False
                    #self.xCoord += self.speed # Move directly right return
                    if self.tracking: # If tracking, generate new DX and DY 
                        self.DX = random.choice([random.uniform(-6, -4), random.uniform(4, 6)])
                        self.DY = 3
                        self.tracking = False
                    bounceHorizontallySpecialSawblade(app, self) 
                    bounceVerticallySpecialSawblade(app, self)

                else:
                    print("Doesn't block")
                    app.canSee = True
                    self.tracking = True
                    self.xCoord += self.speed * (dx / dist) 
                    self.yCoord += self.speed * (dy / dist)
            else:
                self.xCoord += self.speed * (dx / dist) 
                self.yCoord += self.speed * (dy / dist)

def bounceHorizontallySpecialSawblade(app, specialSawblade): 
    specialSawblade.xCoord += specialSawblade.DX 
    if specialSawblade.xCoord + specialSawblade.radius >= app.backgroundX + app.backgroundWidth: 
        specialSawblade.xCoord = (app.backgroundX + app.backgroundWidth) - specialSawblade.radius 
        specialSawblade.DX = -specialSawblade.DX 
    elif specialSawblade.xCoord - specialSawblade.radius <= app.backgroundX: 
        specialSawblade.xCoord = app.backgroundX + specialSawblade.radius 
        specialSawblade.DX = -specialSawblade.DX 

def bounceVerticallySpecialSawblade(app, specialSawblade): 
    specialSawblade.yCoord += specialSawblade.DY 
    if specialSawblade.yCoord + specialSawblade.radius >= app.backgroundY + app.backgroundHeight: 
        specialSawblade.yCoord = (app.backgroundY + app.backgroundHeight) - specialSawblade.radius 
        specialSawblade.DY = -specialSawblade.DY # Optional: Remove special sawblades if they go out of bounds (example logic) 
        
        for specialSawblade in app.specialSawblade: 
            if specialSawblade.yCoord + specialSawblade.radius + 100 <= 0: 
                app.specialSawblade.remove(specialSawblade)

def main():
    runApp(width = 400, height = 500)

main()

    