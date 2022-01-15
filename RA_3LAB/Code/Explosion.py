import pygame
from random import choice

class Explosion(pygame.sprite.Sprite):
    def __init__(self, size, position):
        super().__init__()
        # setting the meteor size, position, images
        self.size = size
        self.images = []
        self.explosion_type = choice(['sonic', 'regular']) # choosing the explosion type

        for i in range(9):
            self.images.append(pygame.transform.scale(pygame.image.load('../Graphics/' + self.explosion_type + 'Explosion0' + i.__str__() +'.png'), (self.size, self.size)))

        self.image = self.images[0]
        self.rect = self.image.get_rect(center= position)

        self.frame = 0 # setting the first frame
        self.last_update = pygame.time.get_ticks() # setting the last explosion update
        self.frame_rate = 90 # setting the explosion time

        # setting and playing the explosion sound
        self.explosion_sound = choice([pygame.mixer.Sound('../Audio/expl1.wav'), pygame.mixer.Sound('../Audio/expl2.wav')])
        self.explosion_sound.play()

    def update(self):

        current_time = pygame.time.get_ticks() # getting the current time

        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time # setting the new last update
            self.frame += 1 # setting the new frame

            # setting the new frame as an image
            if self.frame == 9:
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center = center)
