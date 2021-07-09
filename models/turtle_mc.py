import pygame
import src
import view
from models import hit_box

TURTLE_ALIVE = 0
TURTLE_DYING = 1
TURTLE_DIED = 2

class TurtleMC(pygame.sprite.Sprite):

    def __init__(self, Ratio, window_width, window_Height):
        pygame.sprite.Sprite.__init__(self)

        # 參考首張圖片的size
        self.refImage = pygame.image.load("src/Turtle-0-down.png").convert_alpha()
        self.refImageWidth, self.refImageHeight = self.refImage.get_size()
        # 海龜height = 視窗height * Ratio
        # 海龜Width = 海龜height * refImageRatio
        self.image_height = int(window_Height * Ratio)
        self.image_width = int(self.image_height * self.refImageWidth / self.refImageHeight)
        del self.refImage, self.refImageWidth, self.refImageHeight

        self.chg_image_cnter = 0
        self.chg_image_threshold = 10
        self.image_index = 0
        self.alive_images = [pygame.transform.scale((pygame.image.load("src/Turtle-0-down.png").convert_alpha()), (self.image_width ,self.image_height)),
                pygame.transform.scale((pygame.image.load("src/Turtle-0-up.png").convert_alpha()), (self.image_width ,self.image_height))]
        self.dying_images = [pygame.transform.scale((pygame.image.load("src/Turtle-1-down.png").convert_alpha()), (self.image_width ,self.image_height)),
                pygame.transform.scale((pygame.image.load("src/Turtle-1-up.png").convert_alpha()), (self.image_width ,self.image_height))]
        self.died_image = pygame.transform.scale((pygame.image.load("src/Turtle-die.png").convert_alpha()), (self.image_width ,self.image_height))
        self.images = self.alive_images
        self.image_amt = len(self.images)
        self.image = self.images[self.image_index]

        self.window_width = window_width
        self.window_height = window_Height
        self.frame = 20
        self.rect = self.image.get_rect()
        self.rect.x = self.frame
        self.rect.y = (window_Height - self.image_height)/2
        self.step = 15

        # 新增頭部 hitBox sprite
        self.hit_box = hit_box.HitBox(int(self.rect.x + self.image_width * (2/5)),
                self.rect.y,
                int(self.image_width * (3/7)),
                int(self.image_height * (2/5)))

    # def move(self, direction): # 以海龜全身為hit box
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
    #     self.chg_image()
    #     # hitBox sprite 跟隨 turtle sprite
    #     self.hitBox.rect.update(int(self.rect.x + self.imageWidth * (2/5)),
    #             self.rect.y,
    #             int(self.imageWidth * (3/7)),
    #             int(self.imageHeight * (2/5)))


    def move(self, direction): # 以海龜頭部為hit box
        # 移動
        if direction == "right":
            if self.hit_box.rect.x + self.hit_box.rect.width < self.window_width:
                self.rect.x += self.step
        elif direction == "left":
            if self.hit_box.rect.x > 0:
                self.rect.x -= self.step
        elif direction == "up":
            if self.hit_box.rect.y > 0:
                self.rect.y -= self.step
        elif direction == "down":
            if self.hit_box.rect.y + self.hit_box.rect.height < self.window_height:
                self.rect.y += self.step
        elif direction == "stop":
            self.rect.x = self.rect.x
            self.rect.y = self.rect.y
        self.chg_image()

        # hitBox sprite 跟隨 turtle sprite
        self.hit_box.rect.update(int(self.rect.x + self.image_width * (2/5)),
                self.rect.y,
                int(self.image_width * (3/7)),
                int(self.image_height * (2/5)))

    # 換圖片
    def chg_image(self):
        # 如果 image amount 不足以換圖片則不執行
        if self.image_amt <= 1:
            return

        self.chg_image_cnter += 1
        if self.chg_image_cnter >= self.chg_image_threshold:
            self.chg_image_cnter = 0
            self.image_index += 1
            if self.image_index >= self.image_amt:
                self.image_index = 0
            self.image = self.images[self.image_index]

    # num = 0 活好好的
    # num = 1 插一根吸管
    def set_image(self, state):
        print("turtle state {}".format(state))
        if state == TURTLE_ALIVE:
            self.images = self.alive_images
            self.image_amt = len(self.images)
            self.image = self.images[self.image_index]
        elif state == TURTLE_DYING:
            self.images = self.dying_images
            self.image_amt = len(self.images)
            self.image = self.images[self.image_index]
        else:
            self.image = self.died_image
            self.image_amt = 1
