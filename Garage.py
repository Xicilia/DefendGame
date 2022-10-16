import sys
import pygame
from GUI import FollowingHealthBar
from Sprite import Sprite
from constants import COLORS, DOWNPOS


class Garage(Sprite):

    def __init__(self, spriteFile, gameObject, HP, **kwargs):
        garagePos = (
            gameObject.width / 2,
            gameObject.height / 2
        )
        super().__init__(spriteFile, garagePos, gameObject)
        
        self.HP = HP
        
        self.HPBar = FollowingHealthBar(
            self.gameObject,
            COLORS["WHITE"],
            spriteToFollow=self,
            POS=DOWNPOS,
            HP=self.HP,
            text=kwargs["text"]
        )
        
    def show(self):
        super().show()
        self.HPBar.show()
    
    def getHit(self, damage):
        self.HP -= damage
        
        if self.HP <= 0:
            pygame.quit()
            sys.exit()
        
        self.HPBar.updateHp(self.HP)
