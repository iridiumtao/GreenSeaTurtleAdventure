import pygame
import random
import time
import src
import view

class TurtleMC(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, image1, image2, image3, image4, num):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale((pygame.image.load(image).convert_alpha()), (w,h))

        self.image1 = pygame.transform.scale((pygame.image.load(image1).convert_alpha()), (w,h))
        self.image2 = pygame.transform.scale((pygame.image.load(image2).convert_alpha()), (w,h))
        self.image3 = pygame.transform.scale((pygame.image.load(image3).convert_alpha()), (w,h))
        self.image4 = pygame.transform.scale((pygame.image.load(image4).convert_alpha()), (w,h))

        #self.images =[self.image,self.image1,self.image2,self.image3,self.image4]

        self.flapIndex = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.height = h
        self.direction = "right"
        self.num = num


         
     
    '''
     def changeDirection(self):
         if self.rect.x >= (1280/2)+100 and self.rect.x < 1300:
            self.direction = random.choice(["right","left"])
         elif (self.rect.x < (1280/2)+100):
            self.direction = "right"
            self.image1 = pygame.transform.flip(self.image1, True, False)
            self.image2 = pygame.transform.flip(self.image2, True, False)
            self.image3 = pygame.transform.flip(self.image3, True, False)
            self.image4 = pygame.transform.flip(self.image4, True, False)
         elif self.rect.x > 1700-100:
            self.direction = "left"
    '''

    def update(self):
        if self.flapIndex != -1:
            #self.flap()
            self.rect.x += self.num
            print("move")

    
    def flap(self):
        pass
        
        # if (self.flapIndex != -1):
        #     if (self.flapIndex == 2):
        #        self.flapIndex = 0
        #     self.image = self.images[self.flapIndex]
        #     self.flapIndex += 1
        

