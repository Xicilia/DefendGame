import pygame
from Rocket import Rocket
from constants import ATTACKPRESSEDWITHNOTENOUGHTIMEELAPSED, HITTINGSPRITECOLLIDEWITHBOMJ, PLAYERSPRITEWIDTH, PLAYERSPRITEHEIGHT, LEFTDIRECTION, RIGHTDIRECTION, COLORS, PLAYERNAME, DOWNPOS, ULTPRESSEDWITHNOTENOUGHTIMEELAPSED, \
    UPPOS, HITTINGSPRITECOLLIDEWITHGARAGE
from transform import transformSpriteToConstSize
from Weapon import getWeapon, Gun
from GUI import FollowingLabel, FollowingLabelFulling, Label, VanishingLabel
from Sprite import Sprite


class Player(Sprite):

    def __init__(self, startPos, spriteFile, speed, gameObject):

        super().__init__(spriteFile, startPos, gameObject)

        if self.image.get_width() > PLAYERSPRITEWIDTH and self.image.get_height() > PLAYERSPRITEHEIGHT:
            self.image = transformSpriteToConstSize(self.image, PLAYERSPRITEWIDTH, PLAYERSPRITEHEIGHT)

        self.speed = speed

        self.direction = LEFTDIRECTION

        self.weapon = getWeapon("eupistol", self, self.gameObject)
        gameObject.addSprite(self.weapon)

        self.nameLabel = FollowingLabel(
            self.gameObject,
            COLORS["WHITE"],
            0, #pos
            PLAYERNAME,
            self,
            DOWNPOS
        )

        self.nameLabel.show()

        self.currentPhrase = None
        
        self.ultCharge = 0
        self.ultLabel = Label(
            self.gameObject,
            COLORS["BLACK"],
            0,
            f"Заряд ульты: {self.ultCharge}%"
        )
        ultLabelSize = self.ultLabel.getSize()
        self.ultLabel.changePos((
            0, self.gameObject.height - ultLabelSize[1]
        ))
        self.ultLabel.show()
        
        self.notEnoughTimeElapsedLabel = None

    def useUlt(self):
        Rocket(
            self.gameObject.resources["ROCKET"],
            (self.rect.x if self.direction == LEFTDIRECTION else self.rect.x + self.rect.w,
             self.rect.y + (self.rect.h / 2)),
            self.gameObject,
            8,
            self
        ).launch()

    def update(self):

        keys = pygame.key.get_pressed()

        for event in self.gameObject.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    if self.weapon.hided:
                        self.weapon.show()
                    else:
                        self.weapon.hide()
                elif event.key == pygame.K_q:
                    if not self.weapon.hided:
                        self.weapon.use()

                elif event.key == pygame.K_r:
                    if self.weapon.__class__ is Gun:
                        self.weapon.reload()
                
                elif event.key == pygame.K_f:
                    if self.ultCharge >= 100:
                        self.useUlt()
                        self.ultCharge = 0
                        self.ultLabel.changeText(f"Заряд ульты: {self.ultCharge}%")
                    else:
                        pygame.event.post(pygame.event.Event(ULTPRESSEDWITHNOTENOUGHTIMEELAPSED))
                        
            elif event.type == HITTINGSPRITECOLLIDEWITHGARAGE and not self.currentPhrase:
                self.currentPhrase = FollowingLabelFulling(
                    self.gameObject,
                    COLORS["WHITE"],
                    0,
                    "Блять это же мой гаражжж",
                    self,
                    UPPOS
                )
                self.currentPhrase.show()
                
            elif event.type == HITTINGSPRITECOLLIDEWITHBOMJ:
                if self.ultCharge < 100 and event.projectile is not Rocket:
                    self.ultCharge += event.damage * 3
                    self.ultCharge = 100 if self.ultCharge > 100 else self.ultCharge
                    self.ultLabel.changeText(f"Заряд ульты: {self.ultCharge}%")
                    
            elif event.type == ATTACKPRESSEDWITHNOTENOUGHTIMEELAPSED:
                if self.notEnoughTimeElapsedLabel and not self.notEnoughTimeElapsedLabel.hided:
                    self.notEnoughTimeElapsedLabel.hide()
                    
                self.notEnoughTimeElapsedLabel = VanishingLabel(
                    self.gameObject,
                    COLORS["WHITE"],
                    (0, 0),
                    "Я НЕ МОГУ ЕМАЕЕЕЕЕ",
                    500
                )
                
                size = self.notEnoughTimeElapsedLabel.getSize()
                self.notEnoughTimeElapsedLabel.changePos(
                    (
                        self.gameObject.width / 2 - (size[0] / 2),
                        self.gameObject.height - size[1]
                    )
                )
                
                self.notEnoughTimeElapsedLabel.show()
            elif event.type == ULTPRESSEDWITHNOTENOUGHTIMEELAPSED:
                if self.notEnoughTimeElapsedLabel and not self.notEnoughTimeElapsedLabel.hided:
                    self.notEnoughTimeElapsedLabel.hide()
                    
                self.notEnoughTimeElapsedLabel = VanishingLabel(
                    self.gameObject,
                    COLORS["WHITE"],
                    (0, 0),
                    "МНЕ НЕ ХВАТАЕТ АААА",
                    500
                )
                
                size = self.notEnoughTimeElapsedLabel.getSize()
                self.notEnoughTimeElapsedLabel.changePos(
                    (
                        self.gameObject.width / 2 - (size[0] / 2),
                        self.gameObject.height - size[1]
                    )
                )
                
                self.notEnoughTimeElapsedLabel.show()
                    
                    

        leftPressed = keys[pygame.K_a]
        rightPressed = keys[pygame.K_d]

        garage = self.gameObject.level.garage.rect

        allowedXMovement = True
        allowedYMovement = True
        
        if leftPressed:
            
            probRect = self.rect.copy()
            probRect.x += -self.speed * leftPressed
            
            if probRect.colliderect(garage):
                allowedXMovement = False
        elif rightPressed:
            
            probRect = self.rect.copy()
            probRect.x += self.speed * rightPressed
            
            if probRect.colliderect(garage):
                allowedXMovement = False
                
        if keys[pygame.K_w]:
            
            probRect = self.rect.copy()
            probRect.y += -self.speed * keys[pygame.K_w]
            
            if probRect.colliderect(garage):
                allowedYMovement = False
        elif keys[pygame.K_s]:
            
            probRect = self.rect.copy()
            probRect.y += self.speed * keys[pygame.K_s]
            
            if probRect.colliderect(garage):
                allowedYMovement = False
        

        lastPos = (self.rect.x, self.rect.y)
        
        self.rect.move_ip(
            (-self.speed * leftPressed + self.speed * rightPressed) * allowedXMovement,
            (-self.speed * keys[pygame.K_w] + self.speed * keys[pygame.K_s]) * allowedYMovement
        )

        if self.rect.colliderect(garage):
            self.rect.x = lastPos[0]
            self.rect.y = lastPos[1]
            
        
        if self.rect.x + self.rect.width > self.gameObject.width: 
            self.rect.x = self.gameObject.width - self.rect.width
        elif self.rect.x < 0:
            self.rect.x = 0 
        
        if self.rect.y + self.rect.height > self.gameObject.height:
            self.rect.y = self.gameObject.height - self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0

        if leftPressed:
            self.direction = LEFTDIRECTION
        elif rightPressed:
            self.direction = RIGHTDIRECTION
            
        if self.currentPhrase and self.currentPhrase.hided == True:
            self.currentPhrase = None
