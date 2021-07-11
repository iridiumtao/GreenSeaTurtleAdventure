import pygame
import random
import time
import assests
import src.view as view

class Straw(pygame.sprite.Sprite):
    # def __init__(self, maxWidth, x=10, y=200, h=70, w=20, image="assests/straw.png"):
    def __init__(self, maxWidth, maxHeight, h=70, w=20, image="assests/straw.png"):
        pygame.sprite.Sprite.__init__(self)

        self.maxWidth = maxWidth
        self.maxHeight = maxHeight - w

        self.image1 = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (w,h))
        self.image2 = pygame.transform.rotate(self.image1, 90)
        self.image3 = pygame.transform.flip(self.image2, True, False)

        self.image = self.image3
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(self.maxWidth, self.maxWidth * 2)
        self.rect.y = random.randint(0, self.maxHeight)

    def update(self):
        '''
        object moves horizontally left and starts again after out of screen
        '''
        self.rect.x -= 10
        if self.rect.x < -10:
            self.rect.x = self.maxWidth + 10
            self.rect.y = random.randint(0, self.maxHeight)
