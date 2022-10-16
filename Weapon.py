import pygame
from Bomj import Bomj
from constants import ATTACKPRESSEDWITHNOTENOUGHTIMEELAPSED, WEAPONWIDTH, WEAPONHEIGHT, LEFTDIRECTION, RIGHTDIRECTION, THROWABLEWEAPONSPEED, BULLETSPEED, \
    COLORS, HITTINGSPRITECOLLIDEWITHBOMJ, HITTINGSPRITECOLLIDEWITHGARAGE
from transform import transformSpriteToConstSize, flipSprite
from GUI import Label, VanishingLabel
from Sprite import Sprite, HittingSprite
#from sprites import WEAPONSPRITES, BULLET

WEAPONS = {
    "test": {
        "type": "throwable",
        "sprite": "WEAPONTEST",
        "damage": 2
    },
    "eupistol": {
        "type": "gun",
        "sprite": "EUPISTOL",
        "damage": 4,
        "ammoSize": 7
    }
}


def getWeapon(weaponName, player, gameObject):
    if weaponName in WEAPONS:
        currentWeapon = WEAPONS[weaponName]

        weaponType = currentWeapon["type"]
        if weaponType == "throwable":
            return Throwable(
                gameObject.resources[currentWeapon["sprite"]],
                player,
                currentWeapon["damage"],
                gameObject
            )
        elif weaponType == "gun":
            return Gun(
                gameObject.resources[currentWeapon["sprite"]],
                player,
                currentWeapon["damage"],
                gameObject,
                currentWeapon["ammoSize"]
            )


class Weapon(Sprite):

    def __init__(self, spriteFile, player, damage, gameObject, Transform=True):

        super().__init__(spriteFile, (0, 0), gameObject)

        if Transform:
            self.image = transformSpriteToConstSize(
                self.image,
                WEAPONWIDTH,
                WEAPONHEIGHT
            )

        self.player = player
        self.direction = LEFTDIRECTION

        self.updatePosition()

        self.damage = damage

        self.used = False

        self.hided = False

    def use(self):
        self.used = True

    def action(self):
        pass

    def updatePosition(self):

        widthOffset = (self.player.rect.width / 2) - (self.rect.width / 2)  # start offset calculated from width
        heightOffset = (self.player.rect.height / 2) - (self.rect.height / 2)
        directionOffset = 43 * self.player.direction

        if self.direction != self.player.direction:
            self.image = flipSprite(self.image, True, False)

        self.rect.x = self.player.rect.x + widthOffset + directionOffset
        self.rect.y = self.player.rect.y + heightOffset

        self.direction = self.player.direction

    def update(self):
        if self.used:
            self.action()
        else:
            self.updatePosition()

    def delete(self):
        self.hide()
        self.player.weapon = None

    def hide(self):
        super().hide()
        self.hided = True

    def show(self):
        super().show()
        self.hided = False


class Throwable(Weapon):

    def __init__(self, spriteFile, player, damage, gameObject):
        super().__init__(spriteFile, player, damage, gameObject)

        self.throwed = None

    def refresh(self):
        self.used = False
        self.show()

    def use(self):
        if not self.used:
            self.used = True
            ThrowedSprite(
                self.gameObject,
                self,
                self.direction,
                self.damage,
                self.refresh
            )
            self.hide()


class ThrowedSprite(HittingSprite):

    def __init__(self, gameObject, weapon, direction, damage, onReach = None):
        super().__init__(
            weapon.image, 
            (weapon.rect.x, weapon.rect.y),
            gameObject,
            damage
        )

        #self.gameObject = gameObject

        self.gameObject.addSprite(self)

        #self.image = weapon.image

        self.rect = weapon.rect

        self.originalImage = self.image.copy()

        self.rot = 0

        self.rot_speed = 50

        self.direction = direction

        self.lastUpdate = self.gameObject.now

        self.onReach = onReach

    def update(self):
        now = self.gameObject.now

        if now - self.lastUpdate > 50:
            self.lastUpdate = now

            self.rot = (self.rot + (self.rot_speed * -self.direction)) % 360
            self.image = pygame.transform.rotate(self.originalImage, self.rot)

        self.rect.move_ip(THROWABLEWEAPONSPEED * self.direction, 0)

        super().update()
            
    def onHit(self, hitObject):
        if hitObject.__class__ is Bomj:
            hitObject.hit(self.damage)
        if self.onReach: self.onReach()
        self.hide()


class Gun(Weapon):

    def __init__(self, spriteFile, player, damage, gameObject, ammo):
        super().__init__(spriteFile, player, damage, gameObject)

        self.ammoSize = ammo

        self.ammo = self.ammoSize

        self.shotDelay = 0

        self.active = True

        self.ammoLabel = Label(
            gameObject,
            COLORS["BLACK"],
            0,  # size
            self._getAmmoText())

        labelSize = self.ammoLabel.getSize()
        self.ammoLabel.changePos(
            (
                self.gameObject.width - labelSize[0],
                self.gameObject.height - labelSize[1]
            )
        )

        self.gameObject.addGuiElement(self.ammoLabel)
        
        self.delayAfterThrow = 2500
        self.lastThrowTime = 0
        self.notEnoughTimeElapsedLabel = None

    def updateAmmoText(self):
        self.ammoLabel.changeText(self._getAmmoText())

    def _getAmmoText(self):
        return f"{self.ammo}/{self.ammoSize}"

    def use(self):
        # shot or reload if ammo is empty
        now = self.gameObject.now
        
        if self.ammo:
            if now - self.shotDelay > 500:
                self.shot()
                self.ammo -= 1

                self.updateAmmoText()

                self.shotDelay = now
        else:
            self.reload()

    def shot(self):
        if not self.active:
            return

        Bullet(
            self.gameObject.resources["BULLET"],
            self.gameObject,
            self.damage, self.direction,
            (self.rect.x, self.rect.y),
            (self.rect.width, self.rect.height)
        )

    def delete(self):
        super().delete()
        self.gameObject.removeGuiElement(self.ammoLabel)

        if self.ammo != self.ammoSize:
            self.player.hidedAmmo = self.ammo

    def show(self):
        if not self.active:
            return

        super().show()
        self.ammoLabel.show()

    def hide(self):
        super().hide()
        self.ammoLabel.hide()

    def refresh(self):
        self.active = True
        self.show()

    def reload(self):
        now = self.gameObject.now
        
        if not self.active:
            if now - self.lastThrowTime > self.delayAfterThrow:
                self.refresh()
            else:
                pygame.event.post(pygame.event.Event(ATTACKPRESSEDWITHNOTENOUGHTIMEELAPSED))
            return
        
        self.active = False
        self.hide()

        ThrowedSprite(
            self.gameObject,
            self,
            self.direction,
            self.damage
        )

        self.lastThrowTime = now

        self.ammo = self.ammoSize
        self.updateAmmoText()

    def update(self):
        super().update()
           

class Bullet(HittingSprite):

    def __init__(self, spriteFile, gameObject, gunDamage, direction, gunPosition, gunSize):

        super().__init__(spriteFile, (0, 0), gameObject, gunDamage)

        self.direction = direction

        self.rect = self.image.get_rect(center=(
            gunPosition[0] + (gunSize[0] / 2) * self.direction, gunPosition[1] + (gunSize[1] / 2)
        ))

        self.damage = gunDamage

        if self.direction == RIGHTDIRECTION:
            self.image = flipSprite(self.image, True, False)

        self.gameObject = gameObject
        self.gameObject.addSprite(self)
        
        self.alreadyHitSomeone = False

    def update(self):
        self.rect.move_ip(BULLETSPEED * self.direction, 0)
        
        super().update()
        
    def onHit(self, hitObject):
        if not self.alreadyHitSomeone:
            if hitObject.__class__ is Bomj:
                hitObject.hit(self.damage)
            self.hide()
            self.alreadyHitSomeone = True