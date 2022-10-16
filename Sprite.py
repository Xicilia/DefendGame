import pygame
from constants import HITTINGSPRITECOLLIDEWITHGARAGE, HITTINGSPRITECOLLIDEWITHBOMJ, WALLHIT

class Sprite(pygame.sprite.Sprite):

    def __init__(self, spriteFile, startPos, gameObject):

        pygame.sprite.Sprite.__init__(self)

        if type(spriteFile) is str:
            self.image = pygame.image.load(spriteFile).convert_alpha()
        else:
            self.image = spriteFile.copy()

        self.rect = self.image.get_rect(center=startPos)

        self.gameObject = gameObject

    def show(self):
        
        self.gameObject.addSprite(self)

    def hide(self):
        
        self.gameObject.removeSprite(self)

    def update(self):
        pass
    
class HittingSprite(Sprite):
    
    def __init__(self, spriteFile, startPos, gameObject, damage):
        super().__init__(spriteFile, startPos, gameObject)
         
        self.damage = damage
        
    def update(self):
        if self.rect.x > self.gameObject.width + self.rect.width or self.rect.x < -self.rect.width:
            self.onHit(WALLHIT)
            
        if self.gameObject.level:
            
            if self.rect.colliderect(self.gameObject.level.garage.rect):
                pygame.event.post(pygame.event.Event(HITTINGSPRITECOLLIDEWITHGARAGE))
                
            for bomj in self.gameObject.level.currentBomjes:
                
                if self.rect.colliderect(bomj):
                    pygame.event.post(pygame.event.Event(HITTINGSPRITECOLLIDEWITHBOMJ, damage=self.damage, projectile=self.__class__))
                
                    self.onHit(bomj)
                    
    def onHit(self, hitObject):
        pass
