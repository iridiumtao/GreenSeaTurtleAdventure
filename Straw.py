import pygame
import random
import time
import src
import view

class Straw(pygame.sprite.Sprite):
    def __init__(self, maxWidth, x=10, y=200, h=70, w=20, image="src/straw.png"):
        pygame.sprite.Sprite.__init__(self)


        self.image1 = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (w,h))
        self.image2 = pygame.transform.rotate(self.image1, 90)
        self.image3 = pygame.transform.flip(self.image2, True, False)


        self.image = self.image3
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        
        self.maxWidth = maxWidth
    
    '''def changeDir(self):

        if self.rect.x < -30:
            self.dir = "right"
            self.image1 = pygame.transform.flip(self.image1, True, False)
            self.image2 = pygame.transform.flip(self.image2, True, False)
        if self.rect.x > 1700:
            self.dir = "left"
            self.image1 = pygame.transform.flip(self.image1, True, False)
            self.image2 = pygame.transform.flip(self.image2, True, False)'''
    
    def update(self):

    	self.rect.x -= 10
    	if self.rect.x < -10:
    		self.rect.x = self.maxWidth + 10


