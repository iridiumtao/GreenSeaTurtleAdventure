import pygame
import random
import time
import src
import view

class TurtleMC(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, windowWidth, windowHeight):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale((pygame.image.load("src/Turtle-0-down.png").convert_alpha()), (w,h))
        self.flapIndex = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.height = h
        self.widthOffset = -50
        self.heightOffset = 0
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.step = 10

    def move(self, direction):
        if direction == "right":
            if self.rect.x + self.width < self.windowWidth:
                self.rect.x += self.step
        elif direction == "left":
            if self.rect.x > 0 + self.widthOffset:
                self.rect.x -= self.step
        elif direction == "up":
            if self.rect.y > 0 + self.heightOffset:
                self.rect.y -= self.step
        elif direction == "down":
            if self.rect.y + self.height < self.windowHeight:
                self.rect.y += self.step