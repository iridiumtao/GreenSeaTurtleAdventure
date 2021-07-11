import configparser
import pygame
import os

class LocalConfig(object):
    """
    Ues configparser to generate or load config from config.ini file
    """

    def generate_config(self):
        """
        生成 config.ini
        """
        config = configparser.ConfigParser(allow_no_value=True)
        config['SCREEN'] = {'RESOLUTION_WIDTH' : '1280',
                            'RESOLUTION_HEIGHT' : '720',
                            '# 將全螢幕設為TRUE可能會造成系統解析度的問題' : None,
                            '# Set fullscreen to TRUE may cause some problem on system resolution.' : None,
                            'FULLSCREEN' : 'FALSE',
                            'SCALED' : 'TRUE',
                            'NOFRAME' : 'FALSE',
                            'OPENGL' : 'FALSE',
                            'display_index' : '0',
                            '# 需要開啟OPENGL或SCALED使VSYNC有效' : None,
                            '# VSYNC only works with the OPENGL or SCALED flags set TRUE' : None,
                            'vsync' : '1'}

        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    def load_config(self):
        """
        將 config.ini 的內容載入
        """
        try:
            if not os.path.isfile('config.ini'):
                print("No local config. Loading default.")
                return self.load_default_config()

            config = configparser.ConfigParser()
            config.read('config.ini')

            screen = config['SCREEN']

            resolution_width = int(screen['resolution_width'])
            resolution_height = int(screen['resolution_height'])
            screen_flags = 0
            if screen.getboolean('fullscreen'):
                screen_flags = pygame.FULLSCREEN
            if screen.getboolean('scaled'):
                screen_flags = screen_flags | pygame.SCALED
            if screen.getboolean('noframe'):
                screen_flags = screen_flags | pygame.NOFRAME
            if screen.getboolean('opengl'):
                screen_flags = screen_flags | pygame.OPENGL
            display_index = int(screen['display_index'])
            vsync = int(screen['vsync'])
            return resolution_width, resolution_height, screen_flags, display_index, vsync
        except:
            print("Error reading local config. Loading default.")
            return self.load_default_config()

    def load_default_config(self):
        self.generate_config()
        return 1280, 720, pygame.SCALED, 0, 1
