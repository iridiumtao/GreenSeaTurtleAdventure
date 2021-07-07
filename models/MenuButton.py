import pygame
import random
import time
import src
import view

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0, w = 0, h = 0, image="src/start-button.png"):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (int(w), int(h)))

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
