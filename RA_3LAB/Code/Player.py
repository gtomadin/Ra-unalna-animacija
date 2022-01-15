import pygame
from Laser import Laser

class Player(pygame.sprite.Sprite):

    def __init__(self, position, constraint):
        super().__init__()

        # setting the player size, position, image and radius
        self.image = pygame.image.load('../Graphics/playerShip1_blue.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect(midbottom = position)
        self.radius = 15

        self.speed = 5 # setting the player speed
        self.max_x_constraint = constraint # setting the x constraints

        self.ready = True
        self.last_update = pygame.time.get_ticks() # setting the last laser update
        self.laser_time = 150 # setting the laser time

        self.lasers = pygame.sprite.Group() # initializing the lasers

    # getting keyboard input
    def get_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.last_update = pygame.time.get_ticks()

    def recharge(self):

        current_time = pygame.time.get_ticks() # getting the current time

        if current_time - self.last_update >= self.laser_time and not self.ready:
            self.ready = True # setting ready variable

    def constraint(self):
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -6))


    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()