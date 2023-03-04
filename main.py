import pygame
import sys
import random

# pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19.ttf', 40)

gravity = 0.25
gameActive = True
score = 0
highScore = 0


def drawFloor():
    screen.blit(floorSurface, (floorPositionX, 900))
    screen.blit(floorSurface, (floorPositionX + floorSurface.get_width(), 900))


def createPipe():
    randomPostionPipe = random.choice(pipeHights)
    bottomPipe = pipeSurface.get_rect(midtop=(700, randomPostionPipe))
    topPipe = pipeSurface.get_rect(midbottom=(700, randomPostionPipe - 300))
    return bottomPipe, topPipe


def removePipe(pipe):
    if (pipe.left <= -pipeSurface.get_width()):
        pipes.pop(pipes.index(pipe))


def checkCollision(pipes):
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play()
            return False

    if birdRect.top <= -100 or birdRect.bottom >= 900:
        deathSound.play()
        return False

    return True


def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, -birdSpeedY * 3, 1)
    return newBird


def scoreDisplay():
    if gameActive:
        scoreSurface = gameFont.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(288, 100))
        screen.blit(scoreSurface, scoreRect)
    else:
        scoreSurface = gameFont.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(288, 100))
        screen.blit(scoreSurface, scoreRect)

        highScoreSurface = gameFont.render(
            f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center=(288, 850))
        screen.blit(highScoreSurface, highScoreRect)


def updateScore(score, highScore):
    score += 0.01
    if score > highScore:
        highScore = score

    return {'score': score, 'highScore': highScore}


bgSurface = pygame.image.load('./assets/background-day.png').convert()
bgSurface = pygame.transform.scale2x(bgSurface)

floorSurface = pygame.image.load('./assets/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorPositionX = 0

birdDown = pygame.transform.scale2x(pygame.image.load(
    './assets/bluebird-downflap.png').convert_alpha())
birdMid = pygame.transform.scale2x(pygame.image.load(
    './assets/bluebird-midflap.png').convert_alpha())
birdUp = pygame.transform.scale2x(pygame.image.load(
    './assets/bluebird-upflap.png').convert_alpha())
birdFrames = [birdDown, birdMid, birdUp]
birdFrame = 0
birdSurface = birdFrames[birdFrame]
birdRect = birdSurface.get_rect(center=(100, 512))
birdSpeedY = 0

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipeSurface = pygame.image.load('./assets/pipe-green.png').convert()
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipes = []
pipeHights = [400, 600, 800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

gameOverSurface = pygame.image.load('./assets/message.png').convert_alpha()
gameOverSurface = pygame.transform.scale2x(gameOverSurface)
gameOverRect = gameOverSurface.get_rect(center=(288, 512))

flapSound = pygame.mixer.Sound('./sound/sfx_wing.wav')
deathSound = pygame.mixer.Sound('./sound/sfx_hit.wav')
scoreSound = pygame.mixer.Sound('./sound/sfx_point.wav')
scoreCounter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                birdSpeedY = 0
                birdSpeedY -= 8
                flapSound.play()
            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipes.clear()
                birdRect.center = (100, 512)
                birdSpeedY = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipes.extend(createPipe())
        if event.type == BIRDFLAP:
            birdFrame += 1
            if birdFrame >= len(birdFrames) - 1:
                birdFrame = 0

            birdSurface = birdFrames[birdFrame]
            birdRect = birdSurface.get_rect(center=(100, birdRect.centery))

    screen.blit(bgSurface, (0, 0))

    if gameActive:
        rotatedBird = rotateBird(birdSurface)
        screen.blit(rotatedBird, birdRect)
        birdSpeedY += gravity
        birdRect.centery += birdSpeedY
        gameActive = checkCollision(pipes)

        for pipeRect in pipes:
            removePipe(pipeRect)

            if pipeRect.bottom >= 1024:
                screen.blit(pipeSurface, pipeRect)
            else:
                flipPipe = pygame.transform.flip(pipeSurface, False, True)
                screen.blit(flipPipe, pipeRect)

            pipeRect.centerx -= 5

        score = updateScore(score, highScore)['score']
        highScore = updateScore(score, highScore)['highScore']
        scoreCounter += 1
        if scoreCounter >= 100:
            scoreSound.play()
            scoreCounter = 0
    else:
        screen.blit(gameOverSurface, gameOverRect)

    scoreDisplay()

    floorPositionX -= 1
    drawFloor()
    if (floorPositionX < -576):
        floorPositionX = 0

    pygame.display.update()
    clock.tick(120)
