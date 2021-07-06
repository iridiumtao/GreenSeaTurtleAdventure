import pygame
import random
import time
import src
import view

class Heart(pygame.sprite.Sprite):
    def __init__(self, x=10, y=200, size = 40, image="src/heart.png"):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (size, size))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
