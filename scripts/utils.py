import pygame
import os

BASE_IMG_PATH = 'img/'
color = (0,0,0)

def load_img(path):
    img = pygame.image.load(BASE_IMG_PATH + path)
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_img(path + '/' + img_name))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.frame = 0
        self.img_dur = img_dur
        self.done = False
        self.loop = loop

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) - 1)
            if self.frame >= self.img_dur * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_dur)]