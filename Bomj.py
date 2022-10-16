from cmath import sqrt
from dataclasses import dataclass
from random import random
import pygame
from GUI import FollowingHealthBar, FollowingLabel
from Sprite import Sprite
from constants import DOWNPOS, GARAGEATTACKED, LEFTDIRECTION, RIGHTDIRECTION, COLORS, BOMJSPEED, UPPOS
from transform import flipSprite
import random

class Bomj(Sprite):
    
    def __init__(self, spriteFile, startPos, gameObject, level, bomjType, directionX, directionY, allowedXMovement, allowedYMovement, name):
        super().__init__(spriteFile, startPos, gameObject)
        
        self.directionX = directionX
        if self.directionX == RIGHTDIRECTION:
            self.image = flipSprite(self.image, True, False)
        self.directionY = directionY
        
        self.type = bomjType
        self.hp = 15
        
        self.attackRange = 25
        self.attackDelay = 1000
        self.lastAttackTime = 0
        self.damage = 4
        
        self.level = level
        
        self.speedX = BOMJSPEED if allowedXMovement else 0
        self.speedY = BOMJSPEED if allowedYMovement else 0

        
        self.HPBar = FollowingHealthBar(
            self.gameObject,
            COLORS["BLACK"],
            HP=self.hp,
            spriteToFollow=self,
            POS=DOWNPOS
        )
        self.HPBar.show()
        
        self.nameLabel = FollowingLabel(
            self.gameObject,
            COLORS["WHITE"],
            (0, 0),
            name,
            self,
            UPPOS
        )
        self.nameLabel.show()
                 
        
    def update(self):
        
        distanceToGarage = sqrt( (self.level.garage.rect.x - self.rect.x)**2 + (self.level.garage.rect.y - self.rect.y)**2 )

        if distanceToGarage.real <= self.attackRange:
            now = self.gameObject.now
            
            if now - self.lastAttackTime > self.attackDelay:  
                pygame.event.post(pygame.event.Event(GARAGEATTACKED))
                self.level.garage.getHit(self.damage)
                self.lastAttackTime = now
            
        else:
            self.rect.move_ip(self.speedX * -self.directionX, self.speedY * -self.directionY)          
    
    def hit(self, damage):
        self.hp -= damage
        
        if self.hp <= 0:    
            self.hide()
            self.HPBar.hide()
            self.nameLabel.hide()
            
            self.level.lastBomjSpawnTime = self.gameObject.now
            self.level.currentBomjes.remove(self)
        else:
            self.HPBar.updateHp(self.hp)
            
class BomjNameManager():
    
    def __init__(self, namesFile):
        
        self.names = []
        
        with open(namesFile, "r") as f:
            for line in f:
                self.names.append(line.rstrip())
    
    def getRandomName(self):
        return random.choice(self.names)
    
@dataclass
class BomjSpawnPoint():
    x: int
    y: int
    allowedXMovement: bool
    allowedYMovement: bool