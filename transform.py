import pygame


def transformSpriteToConstSize(sprite, width, height):

    spriteWidth = sprite.get_width()
    spriteHeight = sprite.get_height()

    widthRatio = spriteWidth / width
    heightRatio = spriteHeight / height

    return pygame.transform.scale(sprite, (spriteWidth // widthRatio, spriteHeight // heightRatio) )


def rotateSprite(sprite, angle):
    return pygame.transform.rotate(sprite, angle)


def flipSprite(sprite, x, y):
    return pygame.transform.flip(sprite, x, y)

