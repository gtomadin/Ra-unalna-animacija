import pygame

class Laser(pygame.sprite.Sprite):

    def __init__(self, position, speed):
        super().__init__()

        # setting the meteor size, position, image, speed
        self.image = pygame.image.load('../Graphics/laserRed07.png').convert_alpha()
        self.rect = self.image.get_rect(center = position)
        self.speed = speed

        # setting and playing the laser sound
        self.shoot_sound = pygame.mixer.Sound('../Audio/pew.wav')
        self.shoot_sound.play()

    # destroying the laser when getting out of the screen
    def destroy(self):
        if self.rect.y <= -50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()