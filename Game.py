import random
import pygame
import sys
from Bomj import BomjSpawnPoint
from GUI import Label
from Level import Level
from Player import Player
from constants import COLORS, SIMPLEBOMJ, STANDARDPLAYERPOS, STANDARDPLAYERSPEED

class Game:

    def __init__(self, rootWindow, size, fps):

        self.width = size[0]
        self.height = size[1]

        self.launched = False
        self.paused = False
        self.pauseLabel = Label(
            self,
            COLORS["WHITE"],
            (0, 0),
            "ПАУЗА"
        )
        self.allPauseTime = 0
        self.lastPauseTime = 0
        
        pauseLabelSize = self.pauseLabel.getSize()
        self.pauseLabel.changePos((
            (self.width / 2) - (pauseLabelSize[0] / 2),
            self.height - pauseLabelSize[1]
        ))

        #self._root = pygame.display.set_mode(size)
        self._root = rootWindow
        self._clock = pygame.time.Clock()
        self.fps = fps

        self.now = pygame.time.get_ticks()

        self.sprites = []
        self.GuiElements = []

        self.events = []

        self.resources = {
            # inited sprites
            "EUPISTOL": pygame.image.load("assets/EUpistol.png").convert_alpha(),
            "SPEAR": pygame.image.load("assets/spear.png").convert_alpha(),
            "UAKNIFE": pygame.image.load("assets/UAKnife.png").convert_alpha(),
            "WEAPONTEST": pygame.image.load("assets/weapontest.png").convert_alpha(),
            "BULLET": pygame.image.load("assets/bullet.png").convert_alpha(),
            "PLAYER": pygame.image.load("assets/player.png").convert_alpha(),
            "TESTMAN": pygame.image.load("assets/test.png").convert_alpha(),
            "GARAGE1": pygame.image.load("assets/Garage1.png").convert_alpha(),
            "EuropeanField": pygame.image.load("assets/EuropeanField.png").convert_alpha(),
            "SIMPLEBOMJ": pygame.image.load("assets/TestBomj.png").convert_alpha(),
            "AMOG": pygame.image.load("assets/REDKYMOB.png").convert_alpha(),
            "ROCKET": pygame.image.load("assets/rocket.png").convert_alpha(),
        }
        
        self.levelResources = {
            0: {
                "name": "Европейские поля",
                "background": self.resources["EuropeanField"],
                "bomjCount": 5,
                "maxBomjAtOneTime": 3,
                "allowedBomjTypes": [SIMPLEBOMJ],
                "spawnPoints": [
                    BomjSpawnPoint(0, self.height / 2, True, False),
                    BomjSpawnPoint(self.width, self.height / 2, True, False),
                    BomjSpawnPoint(self.width / 2, 0, False, True),
                    BomjSpawnPoint(self.width / 2, self.height, False, True)                    
                ],
                "bomjSpawnDelay":1500,
            },
        }
        
        self.level = None
        self.levelId = -1

    def _updateGuiElements(self):
        for element in self.GuiElements:
            self._root.blit(element.surface, element.surfacePos)
            if not self.paused: element.handle()

    def addGuiElement(self, GuiElement):
        self.GuiElements.append(GuiElement)

    def removeGuiElement(self, GuiElement):
        self.GuiElements.remove(GuiElement)
        
    def removeAllGuiElements(self):
        self.GuiElements.clear()
        
    def removeAllSprites(self):
        self.sprites.clear()

    def _updateSprites(self):
        for sprite in self.sprites:
            self._root.blit(sprite.image, sprite.rect)
            if not self.paused: sprite.update()

    def addSprite(self, sprite):
        if not sprite:
            raise NotImplementedError
        self.sprites.append(sprite)

    def removeSprite(self, sprite):

        self.sprites.remove(sprite)

    def idle(self):

        while True:
            self.now = pygame.time.get_ticks() - self.allPauseTime
            
            
            if not self.level:
                self._root.fill(COLORS["WHITE"])
            else:
                self._root.blit(self.level.background.image, (0, 0))

            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        
                        if not self.launched: return
                        
                        self.paused = not self.paused
                        if self.paused:
                            self.pauseLabel.show()
                            self.lastPauseTime = self.now
                        else:
                            self.pauseLabel.hide()
                            self.allPauseTime += self.now - self.lastPauseTime
                            self.now = pygame.time.get_ticks() - self.allPauseTime
                            self.lastPauseTime = 0
                    elif event.key == pygame.K_z:
                        self.restart()
                            

                        
            self._updateSprites()
            self._updateGuiElements()

            if self.level and not self.paused:
                self.level.update()
            
            pygame.display.update()
            self._clock.tick(self.fps)

    def restart(self):
        self.removeAllGuiElements()
        self.removeAllSprites()
        
        self.changeLevel(self.levelId)
        self.setupPlayer()
    
    def changeLevel(self, levelId):
        self.levelId = levelId
        levelResources = self.levelResources[self.levelId]
        self.level = Level(self,
            levelResources["name"],
            levelResources["background"],
            bomjCount = levelResources["bomjCount"],
            maxBomjAtOneTime = levelResources["maxBomjAtOneTime"],
            allowedBomjTypes = levelResources["allowedBomjTypes"],
            spawnPoints = levelResources["spawnPoints"],
            bomjSpawnDelay = levelResources["bomjSpawnDelay"]
        )
        self.level.prepareLevel()
        
    def setupPlayer(self):
        player = Player(STANDARDPLAYERPOS, self.resources["PLAYER"], STANDARDPLAYERSPEED, self)
        player.show()
