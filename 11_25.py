from cmu_graphics import *
from PIL import Image
import math
import random
import time
import os

def onAppStart(app):
    app.stepDelay = 20
    app.stepsPerSecond = 32
    app.backgroundX = app.width/2 - 161
    app.backgroundY = app.height/2 - 180
    app.backgroundWidth = 322
    app.backgroundColor = 'white'
    app.backgroundHeight = 360
    app.dy = 0
    app.ay = 1.2
    app.timer = 1920
    app.displayTimer = 60
    app.timerBarX = app.width/2 - 161
    app.timerBarY = 386
    app.timerBarHeight = 9

    app.alive = True

    app.gems = []

    app.sawblades = []
    app.sawbladesLength = 3
    app.sawbladeColor = 'red'
    app.specialSawblade = None
    makeSawblades(app)

    app.starAngle = 0

    app.jumps = 0
    app.jumpHoldTime = 0
    app.maxJumpHoldTime = 12
    app.isHoldingJump = False 

    app.cx = app.width/2
    app.cy = 360
    app.r = 14

    app.score = 0

def redrawAll(app):
    if app.alive:
        drawRect(0, 0, 400, 400, fill = 'lightBlue')
        drawRect(app.backgroundX, app.backgroundY, app.backgroundWidth, app.backgroundHeight, fill = app.backgroundColor)
        drawCircle(app.cx, app.cy, app.r, fill = 'black')
        drawRect(app.backgroundX, 0, app.backgroundWidth, 20, fill = app.backgroundColor)
        drawLabel(app.score, app.width/2 + 5, app.height/2 + 5, size=130, fill = 'grey', bold = True, font='comicSans', opacity=40)
        drawLabel(app.score, app.width/2, app.height/2, size=130, fill = 'red', bold = True, font='comicSans', opacity=40)

        for sawblade in app.sawblades:
            drawStar(sawblade.xCoord, sawblade.yCoord, 20, 8, fill='white', border='black', borderWidth=3, rotateAngle=-app.starAngle, roundness=75)
            drawCircle(sawblade.xCoord, sawblade.yCoord, 10, fill= sawblade.color)

        for gem in app.gems:
            drawCircle(gem.xCoord, gem.yCoord, gem.radius, fill=gem.color, border = 'black')
        
        drawRect(app.timerBarX, app.timerBarY, app.backgroundWidth, app.timerBarHeight, fill = app.backgroundColor)
        drawRect(app.timerBarX, app.timerBarY, ((app.displayTimer / 60) * app.backgroundWidth), app.timerBarHeight, fill = 'yellow')
        drawLabel(app.displayTimer, app.width/2, 390.5, size = 18, fill = 'black', bold = True)
    
    else:
        drawLabel('Game', app.width/2, 120, size = 120, fill = 'red', bold = True, font='comicSans', opacity=40)
        drawLabel('Over!', app.width/2, 240, size = 120, fill = 'red', bold = True, font='comicSans', opacity=40)
        drawLabel(f"Press 'r' to restart", app.width/2, 340, size = 20, fill = 'red', bold = True, font='comicSans', opacity=40)
        
def onKeyPress(app, key):
    if app.alive:
        if key == 'up' and app.jumps < 2:
            if app.jumps == 0:
                app.isHoldingJump = True
                app.jumpHoldTime = 0
                app.dy = -5
            elif app.jumps == 1:
                app.dy = -11
                app.jumps += 1
    else:
        if key == 'r':
            onAppStart(app)

def onKeyRelease(app, key):
    if key == 'up' and app.isHoldingJump:
        app.isHoldingJump = False
        app.jumps += 1

def onKeyHold(app, keys):
    if 'right' in keys:
        app.cx += 7
        if app.cx + app.r > app.backgroundX + app.backgroundWidth:
            app.cx -= 7
            app.cx += ((app.backgroundX + app.backgroundWidth) - app.cx - app.r)
    elif 'left' in keys:
        app.cx -= 7
        if app.cx - app.r < app.backgroundX:
            app.cx += 7
            app.cx -= (app.backgroundX - app.cx + app.r)

def onStep(app):
    if app.isHoldingJump and app.jumps == 0:
        if app.jumpHoldTime < app.maxJumpHoldTime:
            app.jumpHoldTime += 1
            holdFactor = (1 - (app.jumpHoldTime / app.maxJumpHoldTime)) ** 1.65
            app.dy = -6.5 - (6.5 * holdFactor)

    app.dy += app.ay
    app.cy += app.dy 

    if app.cy + app.r > app.backgroundY + app.backgroundHeight:
        app.cy = app.backgroundY + app.backgroundHeight - app.r
        app.dy = 0 
        app.jumps = 0

    if app.cy - app.r < app.backgroundY:
        app.cy = app.backgroundY + app.r
        app.dy = 0

    for sawblade in app.sawblades:
        bounceHorizontally(app, sawblade)
        bounceVertically(app, sawblade)
    
    if len(app.sawblades) < 4:
        if random.random() < 0.03:
            makeSawblades(app)
    
    app.starAngle -= 12

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

    checkPlayerJumpOver(app)
    collisionCheckerBlade(app)
    collisionCheckerGem(app)
    checkTimer(app)

def checkPlayerJumpOver(app):
    sawbladesToRemove = []
    for sawblade in app.sawblades:
        if app.cy + app.r < sawblade.yCoord + 20 and abs(app.cx - sawblade.xCoord) <= 20:
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

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def collisionCheckerBlade(app):
    for sawblade in app.sawblades:
        length = distance(app.cx, app.cy, sawblade.xCoord, sawblade.yCoord)
        if length - 20 - app.r < -5:
            app.alive = False

def collisionCheckerGem(app):
    for gem in app.gems:
        length = distance(app.cx, app.cy, gem.xCoord, gem.yCoord)
        if length - 6 - app.r < 0:
            app.gems.remove(gem)
            app.timer += 32

def bounceHorizontally(app, sawblade):
    sawblade.xCoord += sawblade.sawbladeDX
    if sawblade.xCoord + sawblade.radius >= app.backgroundX + app.backgroundWidth:
        sawblade.xCoord = (app.backgroundX + app.backgroundWidth) - sawblade.radius
        sawblade.sawbladeDX = -sawblade.sawbladeDX
    elif sawblade.xCoord - sawblade.radius <= app.backgroundX:
        sawblade.xCoord = app.backgroundX + sawblade.radius
        sawblade.sawbladeDX = -sawblade.sawbladeDX

def bounceVertically(app, sawblade):
    sawblade.yCoord += sawblade.sawbladeDY

    if sawblade.yCoord + sawblade.radius >= app.backgroundY + app.backgroundHeight:
        sawblade.yCoord = (app.backgroundY + app.backgroundHeight) - sawblade.radius
        sawblade.sawbladeDY = -sawblade.sawbladeDY

    for sawblade in app.sawblades:
        if sawblade.yCoord + sawblade.radius + 100 <= 0:
            app.sawblades.remove(sawblade)

def checkTimer(app):
    if app.displayTimer <= 0:
        app.alive = False

def makeGems(app, sawbladeX, sawbladeY):
    gem = gems(sawbladeX, sawbladeY, 6)
    gem.dy = -10
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
        self.color = 'yellow'
        self.radius = radius
        self.dy = 0
        self.dx = 0

def main():
    runApp()

main()
