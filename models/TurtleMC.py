import pygame
import random
import time
import src
import view

class TurtleMC(pygame.sprite.Sprite):
    def __init__(self, Ratio, windowWidth, windowHeight):
        pygame.sprite.Sprite.__init__(self)

        # 參考首張圖片的size
        self.refImage = pygame.image.load("src/Turtle-0-down.png").convert_alpha()
        self.refImageWidth, self.refImageHeight = self.refImage.get_size()
        # 海龜height = 視窗height * Ratio
        # 海龜Width = 海龜height * refImageRatio
        self.imageHeight = int(windowHeight * Ratio)
        self.imageWidth = int(self.imageHeight * self.refImageWidth / self.refImageHeight)
        del self.refImage, self.refImageWidth, self.refImageHeight

        self.chgImageCnter = 0
        self.imageIndex = 0
        self.images = [pygame.transform.scale((pygame.image.load("src/Turtle-0-down.png").convert_alpha()), (self.imageWidth ,self.imageHeight)),
                pygame.transform.scale((pygame.image.load("src/Turtle-0-up.png").convert_alpha()), (self.imageWidth ,self.imageHeight))]
        self.image = self.images[self.imageIndex]

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = (windowHeight + self.imageHeight)/2    
        self.widthOffset = -50
        self.heightOffset = 0
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.step = 10

    def move(self, direction):
        if direction == "right":
            if self.rect.x + self.imageWidth < self.windowWidth:
                self.rect.x += self.step
        elif direction == "left":
            if self.rect.x > 0 + self.widthOffset:
                self.rect.x -= self.step
        elif direction == "up":
            if self.rect.y > 0 + self.heightOffset:
                self.rect.y -= self.step
        elif direction == "down":
            if self.rect.y + self.imageHeight < self.windowHeight:
                self.rect.y += self.step
        elif direction == "stop":
            self.rect.x = self.rect.x
            self.rect.y = self.rect.y

        # 10 ticks換一次圖片
        self.chgImageCnter += 1
        if self.chgImageCnter > 9:
            self.chgImageCnter = 0
            self.imageIndex += 1
            if self.imageIndex > 1:
                self.imageIndex = 0
            self.image = self.images[self.imageIndex]
