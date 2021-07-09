import pygame
import src
import view
from models import HitBox
class TurtleMC(pygame.sprite.Sprite):
    TURTLE_ALIVE = 0
    TURTLE_DYING = 1
    TURTLE_DIED = 2
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
        self.chgImageThreshold = 10
        self.imageIndex = 0
        self.images = [pygame.transform.scale((pygame.image.load("src/Turtle-0-down.png").convert_alpha()), (self.imageWidth ,self.imageHeight)),
                pygame.transform.scale((pygame.image.load("src/Turtle-0-up.png").convert_alpha()), (self.imageWidth ,self.imageHeight))]
        self.imageAmt = len(self.images)
        self.image = self.images[self.imageIndex]

        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.frame = 20
        self.rect = self.image.get_rect()
        self.rect.x = self.frame
        self.rect.y = (windowHeight - self.imageHeight)/2
        self.step = 15

        # 新增頭部 hitBox sprite
        self.hitBox = HitBox.HitBox(int(self.rect.x + self.imageWidth * (2/5)),
                self.rect.y,
                int(self.imageWidth * (3/7)),
                int(self.imageHeight * (2/5)))

    # def move(self, direction):
    #     # 移動
    #     if direction == "right":
    #         if self.rect.x + self.imageWidth < self.windowWidth - self.frame:
    #             self.rect.x += self.step
    #     elif direction == "left":
    #         if self.rect.x > 0 + self.frame:
    #             self.rect.x -= self.step
    #     elif direction == "up":
    #         if self.rect.y > 0 + self.frame:
    #             self.rect.y -= self.step
    #     elif direction == "down":
    #         if self.rect.y + self.imageHeight < self.windowHeight - self.frame:
    #             self.rect.y += self.step
    #     elif direction == "stop":
    #         self.rect.x = self.rect.x
    #         self.rect.y = self.rect.y
    #     self.chgImage()
    #     # hitBox sprite 跟隨 turtle sprite
    #     self.hitBox.rect.update(int(self.rect.x + self.imageWidth * (2/5)),
    #             self.rect.y,
    #             int(self.imageWidth * (3/7)),
    #             int(self.imageHeight * (2/5)))


    def move(self, direction):
        # 移動
        if direction == "right":
            if self.hitBox.rect.x + self.hitBox.rect.width < self.windowWidth:
                self.rect.x += self.step
        elif direction == "left":
            if self.hitBox.rect.x > 0:
                self.rect.x -= self.step
        elif direction == "up":
            if self.hitBox.rect.y > 0:
                self.rect.y -= self.step
        elif direction == "down":
            if self.hitBox.rect.y + self.hitBox.rect.height < self.windowHeight:
                self.rect.y += self.step
        elif direction == "stop":
            self.rect.x = self.rect.x
            self.rect.y = self.rect.y
        self.chgImage()

        # hitBox sprite 跟隨 turtle sprite
        self.hitBox.rect.update(int(self.rect.x + self.imageWidth * (2/5)),
                self.rect.y,
                int(self.imageWidth * (3/7)),
                int(self.imageHeight * (2/5)))


    def chgImage(self):
        # 換圖片
        if self.imageAmt <= 1:
            return

        self.chgImageCnter += 1
        if self.chgImageCnter >= self.chgImageThreshold:
            self.chgImageCnter = 0
            self.imageIndex += 1
            if self.imageIndex >= self.imageAmt:
                self.imageIndex = 0
            self.image = self.images[self.imageIndex]

    # num = 0 活好好的
    # num = 1 插一根吸管
    def setImageSetNum(self, num = 0):
        print("turtle state {}".format(num))
        if num == 0 or num == 1:
            self.images = [pygame.transform.scale((pygame.image.load("src/Turtle-"+str(num)+"-down.png").convert_alpha()), (self.imageWidth ,self.imageHeight)),
                    pygame.transform.scale((pygame.image.load("src/Turtle-"+str(num)+"-up.png").convert_alpha()), (self.imageWidth ,self.imageHeight))]
            self.imageAmt = len(self.images)
            self.image = self.images[self.imageIndex]
        else:
            self.image = pygame.transform.scale((pygame.image.load("src/Turtle-die.png").convert_alpha()), (self.imageWidth ,self.imageHeight))
            self.imageAmt = 1
