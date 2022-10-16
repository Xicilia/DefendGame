import pygame
from GUI import Button
from Game import Game
from constants import COLORS, WIDTH, HEIGHT, FPS

def clearGame(gameObject):
    gameObject.removeAllGuiElements()
    gameObject.removeAllSprites()

def exitGame(args):
    pygame.event.post(pygame.event.Event(pygame.QUIT))

def debugText(args):
    print(args["textDebug"])
    
def launchGame(args):
    gameObject = args["game"]
    gameObject.removeAllGuiElements()
    gameObject.changeLevel(0)
    gameObject.setupPlayer()

    gameObject.launched = True

def showMenu(gameObject):
    if gameObject.__class__ is dict:
        gameObject = gameObject["game"]
    clearGame(gameObject)

    menuX = gameObject.width / 2

    startButton = Button(
            gameObject,
            COLORS["BLACK"],
            (0, 0),
            150, 25,
            COLORS["RED"],
            COLORS["BLUE"],
            "START",
            launchGame,
            game=gameObject
    )

    startButtonSize = startButton.getSize()
    startButton.changePos(
        (menuX - (startButtonSize[0] / 2),
        200)
    )
    gameObject.addGuiElement(startButton)


    optionsButton = Button(
            gameObject,
            COLORS["BLACK"],
            (0, 0),
            150, 25,
            COLORS["RED"],
            COLORS["BLUE"],
            "OPTIONS",
            showOptions,
            game=gameObject
    )
    optionsButtonSize = optionsButton.getSize()
    optionsButton.changePos(
        (menuX - (optionsButtonSize[0] / 2),
        250)
    )
    gameObject.addGuiElement(optionsButton)

    exitButton = Button(
            gameObject,
            COLORS["BLACK"],
            (0, 0),
            150, 25,
            COLORS["RED"],
            COLORS["BLUE"],
            "EXIT",
            exitGame,
    )
    exitButtonSize = exitButton.getSize()
    exitButton.changePos(
        (menuX - (exitButtonSize[0] / 2),
        300)
    )
    gameObject.addGuiElement(exitButton)

def showOptions(args):
    clearGame(args["game"])

    gameObject = args["game"]

    backButton = Button(
            gameObject,
            COLORS["BLACK"],
            (250, 250),
            150, 25,
            COLORS["RED"],
            COLORS["BLUE"],
            "BACK",
            showMenu,
            game=gameObject
    )
    gameObject.addGuiElement(backButton)

if __name__ == "__main__":
    
    pygame.init()
    pygame.font.init()
    
    pygame.display.set_caption("Kolyae vs Bomji")

    
    rootWindow = pygame.display.set_mode((WIDTH, HEIGHT))
    
    gameWindow = Game(rootWindow, (WIDTH, HEIGHT), FPS)

    showMenu(gameWindow)

    gameWindow.idle()
