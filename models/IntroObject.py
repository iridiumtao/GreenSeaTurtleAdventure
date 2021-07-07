import pygame
import random
import time
import src
import view

class IntroObject(pygame.sprite.Sprite):
    '''
    for big turtle object: 
        w = 858
        h = 672
        x = -1000
        y = 150
        stopX = -400
        rate = 8
        turn = -15
    '''
    def __init__(self, screenWidth, screenHight, w, h, x, y, stopX, rate, turn=0, flip=False, image="src/Turtle-menu.png"):
        pygame.sprite.Sprite.__init__(self)

        self.w = w*(screenWidth//1080)
        self.h = h*(screenHight//720)

        self.image1 = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.w, self.h))
        self.turn = turn
        self.image2 = pygame.transform.rotate(self.image1, turn)
        self.image3 = pygame.transform.flip(self.image2, flip, False)
        self.image = self.image3
        self.rect = self.image.get_rect()

        self.rect.x = x*(screenWidth/1080)
        self.rect.y = y*(screenHight/720)

        self.stopX = stopX
        self.rate = rate

    def update(self):
        if self.rate > 0:
            if self.rect.x < self.stopX:
                self.rect.x += self.rate
        else:
            if self.rect.x > self.stopX:
                self.rect.x += self.rate