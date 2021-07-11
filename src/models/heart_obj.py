import pygame
import random
import time
import assests
import src.view as view

class Heart(pygame.sprite.Sprite):
    # def __init__(self, x=10, y=200, size = 52, image="assests/heart.png"):
    def __init__(self, index, windowWidth, windowHeight, size = 52, image="assests/heart.png"):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (size, size))
        self.rect = self.image.get_rect()

        self.rect.x = index * size
        self.rect.y = windowHeight - size
