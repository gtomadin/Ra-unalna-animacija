import pygame
import random
from random import choice

class Meteor(pygame.sprite.Sprite):
    def __init__(self, size, position, speed_x, speed_y):
        super().__init__()

        # setting the meteor size, position, image and radius
        self.size = size
        self.set_image()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect(center= position)
        self.radius = self.size * 0.7 / 2

        self.set_speed(speed_x, speed_y) # setting the meteor speed

        self.rotation = 0 # setting the rotation
        self.last_update = pygame.time.get_ticks() # setting the last rotation update
        self.rotation_time = 60 # setting the rotation time

        # setting and playing the meteor sound
        self.meteor_sound = pygame.mixer.Sound('../Audio/meteor.wav')
        self.meteor_sound.set_volume(0.1)
        self.meteor_sound.play()



    def update(self):

        self.rotate()

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def set_image(self):
        # setting the meteor image depending on the size
        meteor_type = choice([1, 2]) # choosing the meteor type
        if (self.size == 50):
            self.image_orig = pygame.image.load(
                '../Graphics/meteorBrown_big' + meteor_type.__str__() + '.png').convert_alpha()
        elif (self.size == 40):
            self.image_orig = pygame.image.load(
                '../Graphics/meteorBrown_med' + meteor_type.__str__() + '.png').convert_alpha()
        elif (self.size == 30):
            self.image_orig = pygame.image.load(
                '../Graphics/meteorBrown_small' + meteor_type.__str__() + '.png').convert_alpha()
        elif (self.size == 20):
            self.image_orig = pygame.image.load(
                '../Graphics/meteorBrown_tiny' + meteor_type.__str__() + '.png').convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (self.size, self.size))


    def set_speed(self, speed_x, speed_y):
        # setting the meteor speed depending on the size
        sign = choice([-1, 1]) # choosing the meteor rotation
        if (self.size == 50):
            self.speed_x = random.randrange(10, 12) * speed_x / 10
            self.speed_y = random.randrange(10, 12) * speed_y / 10
            self.rot_speed = random.randrange(8, 10) * sign
        elif (self.size == 40):
            self.speed_x = random.randrange(12, 14) * speed_x / 10
            self.speed_y = random.randrange(12, 14) * speed_y / 10
            self.rot_speed = random.randrange(10, 12) * sign
        elif (self.size == 30):
            self.speed_x = random.randrange(14, 16) * speed_x / 10
            self.speed_y = random.randrange(14, 16) * speed_y / 10
            self.rot_speed = random.randrange(12, 14) * sign
        elif (self.size == 20):
            self.speed_x = random.randrange(16, 18) * speed_x / 10
            self.speed_y = random.randrange(16, 18) * speed_y / 10
            self.rot_speed = random.randrange(14, 16) * sign

    def rotate(self):

        current_time = pygame.time.get_ticks() # getting the current time

        if current_time - self.last_update > self.rotation_time:

            self.last_update = current_time # setting the new last update
            self.rotation = (self.rotation + self.rot_speed) % 360 # setting the rotation

            # getting the new meteor image
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center

            # setting the new meteor image
            self.image = new_image
            self.rect = self.image.get_rect(center = old_center)

    def change_direction_x(self):
        self.speed_x = -self.speed_x

    def change_direction_y(self):
        self.speed_y = -self.speed_y






