import pygame
from Bomj import Bomj
from Sprite import HittingSprite, Sprite
from constants import LEFTDIRECTION, ROCKETSPEED, WALLHIT
from transform import flipSprite

class Rocket(HittingSprite):
    
    def __init__(self, spriteFile, startPos, gameObject, damage, player):
        super().__init__(spriteFile, startPos, gameObject, damage)
        
        self.player = player
        self.speed = ROCKETSPEED
        
        self.direction = self.player.direction
        if self.direction == LEFTDIRECTION:
            self.image = flipSprite(self.image, True, False)
        
        self.alreadyHitBomjes = []
        
    def launch(self):
        self.show()
    
    def update(self):
        self.rect.move_ip(
            self.speed * self.direction, 0
        )
        
        super().update()
    
    def onHit(self, hitObject):
        if hitObject.__class__ is Bomj and hitObject not in self.alreadyHitBomjes:
            hitObject.hit(self.damage)
            self.alreadyHitBomjes.append(hitObject)
        elif hitObject == WALLHIT:
            self.hide()