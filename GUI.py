from turtle import back
import pygame
from constants import COLORS, comicSans, DOWNPOS, UPPOS


class GUIElement:

    def __init__(self, gameObject, textColor, surfacePos):

        self.gameObject = gameObject

        self.textColor = textColor

        self.surfacePos = surfacePos

        self.surface = None

    def changePos(self, newPos):
        self.surfacePos = newPos

    def getSize(self):
        surfRect = self.surface.get_rect()
        return surfRect.width, surfRect.height

    def handle(self):
        #handle events
        pass

    def hide(self):
        self.gameObject.removeGuiElement(self)

    def show(self):
        self.gameObject.addGuiElement(self)


class Label(GUIElement):

    def __init__(self, gameObject, textColor, surfacePos, text):
        super().__init__(gameObject, textColor, surfacePos)

        self.surface = comicSans.render(text, False, self.textColor)

    def changeText(self, newText):
        self.surface = comicSans.render(newText, False, self.textColor)


class VanishingLabel(Label):
    def __init__(self, gameObject, textColor, surfacePos, text, delayAfterWanish):
        super().__init__(gameObject, textColor, surfacePos, text)
        
        self.delay = delayAfterWanish
        self.timeWhenShowed = 0
        
        self.hided = False
        
    def show(self):
        super().show()
        self.timeWhenShowed = self.gameObject.now
        
    def handle(self):
        now = self.gameObject.now
        
        if now - self.timeWhenShowed > self.delay:
            self.hide()
            self.hided = True


class FollowingLabel(Label):

    def __init__(self, gameObject, textColor, surfacePos, text, spriteToFollow, pos):
        super().__init__(gameObject, textColor, surfacePos, text)

        self.following = spriteToFollow

        self.pos = pos

        self.updatePosition()

    def handle(self):
        super().handle()
        self.updatePosition()

    def updatePosition(self):
        size = self.getSize()

        if self.pos == DOWNPOS:
            self.surfacePos = (
                self.following.rect.x + (self.following.rect.width / 2) - (size[0] / 2),
                self.following.rect.y + self.following.rect.height - (size[1] / 2) + 3 
            )
        elif  self.pos == UPPOS:
            self.surfacePos = (
                self.following.rect.x + (self.following.rect.width / 2) - (size[0] / 2),
                self.following.rect.y - size[1]
            )


class FollowingLabelFulling(FollowingLabel):
    
    def __init__(self, gameObject, textColor, surfacePos, text, spriteToFollow, pos):
        super().__init__(gameObject, textColor, surfacePos, text, spriteToFollow, pos)

        self.delay = 50

        self.deleteDelay = 2000

        self.lastUpdate = 0

        self.currentSymbolIndex = 0

        self.text = text

        self.currentText = self.text[self.currentSymbolIndex]
        self.updateText()

        self.reached = False
        self.hided = False

    def updateText(self):
        self.changeText(self.currentText)

    def handle(self):
        super().handle()
        
        now = self.gameObject.now

        if self.reached:
            if now - self.lastUpdate > self.deleteDelay:
                self.hide()
                self.hided = True

        else:
            if now - self.lastUpdate > self.delay:
                self.lastUpdate = now

                self.currentSymbolIndex += 1

                if self.currentSymbolIndex == len(self.text):
                    self.reached = True
                    return

                self.currentText += self.text[self.currentSymbolIndex]
                self.updateText()
                
                
class HealthBar(GUIElement):
    
    def __init__(self, gameObject, textColor, surfacePos, **kwargs):
        super().__init__(gameObject, textColor, surfacePos)
        
        self.width = kwargs["width"] if "width" in kwargs else 50
        self.height = 25
        
        self.HPColor = kwargs["HPColor"] if "HPColor" in kwargs else COLORS["GREEN"]
        self.lostHPColor = kwargs["lostHPColor"] if "lostHPColor" in kwargs else COLORS["RED"]
        
        self.HP = kwargs["HP"]
        
        self.currentHP = self.HP
        
        if "text" in kwargs:
            self.text = Label(
                self.gameObject,
                self.textColor,
                (0, 0),
                kwargs["text"]
            )
            textHeight = self.text.getSize()[1]
            if textHeight > self.height:
                self.height = textHeight
                
        else:
            self.text = None

        
        self.surface = self.renderSurface()

        
    def renderSurface(self):
        currentHPWidthScale = self.currentHP / self.HP
        currentHPWidth = self.width * currentHPWidthScale
        
        lostHPWidthScale = 1 - currentHPWidthScale
        lostHPWidth = self.width * lostHPWidthScale
        
        currentHPSurface = pygame.Surface(
            (currentHPWidth, self.height), pygame.SRCALPHA
        )
        
        lostHPSurface = pygame.Surface(
            (lostHPWidth, self.height), pygame.SRCALPHA    
        )
        
        currentHPSurface.fill(self.HPColor)
        lostHPSurface.fill(self.lostHPColor)
        
        textSize = self.text.getSize()[0] if self.text else 0
        
        surfaceSize = currentHPSurface.get_width() + lostHPSurface.get_width()
        if self.text:
            surfaceSize += textSize
            
            
        surface = pygame.Surface(
            (surfaceSize, self.height), pygame.SRCALPHA
        )
        
        BarStartPosition = 0
        if self.text:
            surface.blit(self.text.surface, (0, 0))
            BarStartPosition = textSize
            
        surface.blit(currentHPSurface, (BarStartPosition, 0))
        surface.blit(lostHPSurface, (currentHPSurface.get_width() + BarStartPosition, 0))
        
        return surface

    def updateHp(self, newHP):
        self.currentHP = newHP
        self.surface = self.renderSurface()        


class FollowingHealthBar(HealthBar):
    
    def __init__(self, gameObject, textColor, **kwargs):
        super().__init__(gameObject, textColor, (0, 0), **kwargs)
        
        self.following = kwargs["spriteToFollow"]
        self.pos = kwargs["POS"]
        
        self.updatePosition()
    
    def updatePosition(self):
        size = self.getSize()

        if self.pos == DOWNPOS:
            self.surfacePos = (
                self.following.rect.x + (self.following.rect.width / 2) - (size[0] / 2),
                self.following.rect.y + self.following.rect.height - (size[1] / 2) + 3 
            )
        elif  self.pos == UPPOS:
            self.surfacePos = (
                self.following.rect.x + (self.following.rect.width / 2) - (size[0] / 2),
                self.following.rect.y - size[1]
            )
    
    def handle(self):
        super().handle()
        
        self.updatePosition()


class Button(GUIElement):
    
    def __init__(self, gameObject, textColor, surfacePos, width, height, backgroundColor, hoverColor, text, Event = None, **EventArgs):
        super().__init__(gameObject, textColor, surfacePos)
        
        self.backgroundColor = backgroundColor
        self.hoverColor = hoverColor
        
        self.currentColor = self.backgroundColor
        
        self.Event = Event
        self.EventArgs = EventArgs
        
        self.label = Label(
            self.gameObject,
            textColor,
            (0, 0),
            text
        )
        
        labelSize = self.label.getSize()
        self.labelWidth = labelSize[0]
        self.labelHeight = labelSize[1]
        
        self.width = width if self.labelWidth < width else self.labelWidth
        self.height = height if self.labelHeight < height else self.labelHeight
        
        self.rect = None
        
        self.renderButton()
    
    def bindEvent(self, Event):
        self.Event = Event
    
    def _isDotInsideButton(self, dot):
        if self.rect.collidepoint(dot[0], dot[1]):
            return True
        
        return False
    
    def renderButton(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill(self.currentColor)
        
        self.surface.blit(self.label.surface, 
                          (
                              (self.width - self.labelWidth) / 2, 
                              (self.height - self.labelHeight) / 2
                          )
                         )

        self.rect = self.surface.get_rect()
        self.rect.x = self.surfacePos[0]
        self.rect.y = self.surfacePos[1]
        #print(self.rect.x)
    
    def handle(self):
        
        for event in self.gameObject.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    if self.Event and self._isDotInsideButton(event.pos):
                        self.Event(self.EventArgs)
                    
            elif event.type == pygame.MOUSEMOTION:
                if self._isDotInsideButton(event.pos):
                    self.currentColor = self.hoverColor
                else:
                    self.currentColor = self.backgroundColor
                self.renderButton()