import random
from Garage import Garage
from Sprite import Sprite
from transform import transformSpriteToConstSize
from GUI import Label
from constants import COLORS, DOWNPOS, LEFTDIRECTION, RIGHTDIRECTION, SIMPLEBOMJ
from Bomj import Bomj, BomjNameManager

def roll(chance):
    rolledNumber = random.randint(0, 100)
    
    if rolledNumber <= chance:
        return True
    return False

class Level:

    def __init__(self, gameObject, name, background, **kwargs):
        
        self.args = kwargs
        
        self.bomjCount = kwargs["bomjCount"] if "bomjCount" in kwargs else None
        self.maxBomjAtOneTime = kwargs["maxBomjAtOneTime"] if "maxBomjAtOneTime" in kwargs else None
        self.allowedBomjTypes = kwargs["allowedBomjTypes"] if "allowedBomjTypes" in kwargs else None
        
        self.gameObject = gameObject

        self.name = Label(self.gameObject,
                          COLORS["WHITE"],
                          (0, 0), # pos
                          name
                          )
        size = self.name.getSize()
        self.name.changePos(((self.gameObject.width / 2) - (size[0] / 2),0))

        self.background = Background(self.gameObject, background)
        
        self.garage = Garage(
            self.gameObject.resources["GARAGE1"], 
            self.gameObject, 
            100,
            POS=DOWNPOS,
            text="Гараж:"
        )
        
        self.spawnPoints = kwargs["spawnPoints"]
        
        self.currentBomjes = []
        self.bomjSpawnDelay = kwargs["bomjSpawnDelay"]
        self.lastBomjSpawnTime = self.gameObject.now 
        
        self.bomjNamesManager = BomjNameManager("assets/BomjNames.txt")

    def prepareLevel(self):
        self.garage.show()
        self.gameObject.addGuiElement(self.name)
    
    def update(self):
        now = self.gameObject.now
        if len(self.currentBomjes) < self.maxBomjAtOneTime:  
            if now - self.lastBomjSpawnTime < self.bomjSpawnDelay: return
            self.spawnNewBomj()
            self.lastBomjSpawnTime = now
            
    def spawnNewBomj(self):
        
        bomjType = random.choice(self.allowedBomjTypes)
        
        spawnPoint = random.choice(self.spawnPoints)
        
        directionX = LEFTDIRECTION if self.garage.rect.x > spawnPoint.x else RIGHTDIRECTION
        directionY = LEFTDIRECTION if self.garage.rect.y > spawnPoint.y else RIGHTDIRECTION
        
        
        if bomjType == SIMPLEBOMJ:
            bomjSprite = self.gameObject.resources["SIMPLEBOMJ"]
        else:
            bomjSprite = None
            
        bomjName =  self.bomjNamesManager.getRandomName()
            
        if roll(5):
            #rare
            bomjSprite = self.gameObject.resources["AMOG"]
            bomjName = "АМОГ!!"
        
        newBomj = Bomj(
            bomjSprite, 
            (spawnPoint.x, spawnPoint.y), 
            self.gameObject, 
            self, 
            bomjType,
            directionX,
            directionY,
            spawnPoint.allowedXMovement,
            spawnPoint.allowedYMovement,
            bomjName
        )
        newBomj.show()
        
        self.currentBomjes.append(newBomj)


class Background(Sprite):

    def __init__(self, gameObject, sprite):
        super().__init__(sprite, (0, 0), gameObject)

        self.image = transformSpriteToConstSize(self.image,
                                                self.gameObject.width,
                                                self.gameObject.height)