# KidsCanCode, 01/14/2022, Game Development with Pygame video series - Shmup game, https://github.com/kidscancode/pygame_tutorials/tree/master/shmup
# Clear Code, 01/14/2022, Creating Space Invaders in Pygame, https://github.com/clear-code-projects/Space-invaders
# Art from http://www.kenney.nl
# Sound from https://www.bfxr.net/ and https://mixkit.co/free-sound-effects/
import pygame, sys
from Player import Player
from Meteor import Meteor
from Explosion import Explosion

from random import choice
from random import randint

class Game:
    def __init__(self):

        # initializing the player
        player_sprite = Player((screen_width/2, screen_height), screen_width)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # initializing the meteors
        self.meteors = pygame.sprite.Group()
        self.meteor_amount = 0
        self.meteor_capcity = 100

        # initializing the explosions
        self.explosions = pygame.sprite.Group()

        self.score = 0 # initializing the score

        self.font = pygame.font.Font('../Font/Pixeled.ttf', 20) # initializing the font

        self.death_sound = pygame.mixer.Sound('../Audio/rumble1.ogg') # initializing the death sound

        self.gameover = False # initializing the game over variable


    def spawn_meteor(self):

        difference = self.meteor_capcity - self.meteor_amount # getting the difference between the amount of meteors on the screen and the capacity of the meteors

        new_meteor_size = randint(3, 5) * 10 # getting a random size for the new meteor

        # creating a new meteor if the size of the new meteor is less then the difference
        if new_meteor_size < difference:
            self.meteor_amount += new_meteor_size # adding the size of the new meteor to the amount of the meteors on the screen

            self.create_meteor(new_meteor_size, randint(60, screen_width-60), 100, choice([-1, 1]), 1)


    def create_meteor(self, size, x, y, speed_x, speed_y):

        # checking if the spawning position of the meteor is correct
        if x < size:
            x = size + 1
        if x > screen_width - size:
            x = screen_width - size -1
        if y < 100:
            y = 100
        if y > screen_height - size:
            y = screen_height - size -1

        # creating the meteor and adding it to the meteor group
        self.meteors.add(Meteor(size, (x, y), speed_x, speed_y))


    def meteor_position_checker(self):

        # checking if the current position of the meteor is correct, if not the direction of the meteor must be changed

        for meteor in self.meteors:
            if meteor.rect.center[0] >= screen_width - meteor.size/2 or meteor.rect.center[0] <= meteor.size/2:
                meteor.change_direction_x()

            if meteor.rect.center[1] >= screen_height - meteor.size/2 or meteor.rect.center[1] <= meteor.size/2:
                meteor.change_direction_y()



    def collision_checks(self):

        # checking the collisions between meteors and lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:

                meteors_hit = pygame.sprite.spritecollide(laser, self.meteors, True)
                if meteors_hit:
                    for meteor in meteors_hit:

                        self.explosions.add(Explosion(meteor.size, meteor.rect.center)) # creating an explosion

                        self.score += (70 - meteor.size) # adding the score

                        # updating the amount of meteors on the screen
                        if meteor.size == 20 and self.meteor_amount > 0:
                            self.meteor_amount -= 10

                        # breaking the meteor in parts
                        if meteor.size >= 30:
                            self.break_meteor(meteor)

                    laser.kill()

        # checking the collisions between meteors and the player
        if self.meteors:
            for meteor in self.meteors:
                if pygame.sprite.spritecollide(meteor, self.player, False, pygame.sprite.collide_circle):
                    self.death_sound.play() # playing the death sound
                    self.gameover = True # setting the gameover variable to true


    def break_meteor(self, meteor):

        # getting the position difference
        x1 = randint(-5, 5)
        y1 = randint(-5, 5)
        x2 = randint(-5, 5)
        y2 = randint(-5, 5)

        # getting the new speed
        speed_x1 = choice([-1, 1])
        speed_y1 = choice([-1, 1])
        speed_x2 = choice([-1, 1])
        speed_y2 = choice([-1, 1])

        if speed_x1 == speed_x2 and speed_y1 == speed_y2:
            speed_x2 = speed_x2 * -1

        # creating two new meteors
        self.create_meteor(meteor.size - 10, meteor.rect.x + x1, meteor.rect.y + y1, speed_x1, speed_y1)
        self.create_meteor(meteor.size - 10, meteor.rect.x + x2, meteor.rect.y + y2, speed_x2, speed_y2)



    def update_meteor_capacity(self):
        self.meteor_capcity += 10



    def display_score(self):
        score_surf = self.font.render(f' score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf, score_rect)


    def run(self):
        self.player.update()
        self.meteors.update()
        self.explosions.update()

        self.meteor_position_checker()
        self.collision_checks()

        self.meteors.draw(screen)
        self.explosions.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.display_score()

    def show_gameover_screen(self):
        # showing the final score
        gameover_surf = self.font.render(f'Your score: {self.score}', False, 'blue')
        gameover_rect = gameover_surf.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(gameover_surf, gameover_rect)

        # showing the 'press any key' text
        new_game_surf = self.font.render('Press any key', False, 'blue')
        new_game_rect = new_game_surf.get_rect(center=(screen_width / 2, 3 * screen_height / 4))
        screen.blit(new_game_surf, new_game_rect)

        pygame.display.flip()

        # waiting for the player to press any key
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    clock.tick(1000)
                    waiting = False




if __name__ == '__main__':

    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption('Space Game')

    screen_width = 600
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    game = Game()

    # setting the update_capacity timer
    UPDATE_CAPACITY = pygame.USEREVENT + 1
    pygame.time.set_timer(UPDATE_CAPACITY, 8000)

    # setting the spawn_meteor timer
    SPAWN_METEORS = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_METEORS, 1000)

    # setting the background
    background = pygame.image.load('../Graphics/starfield.png').convert_alpha()
    background_rect = background.get_rect()

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == UPDATE_CAPACITY:
                game.update_meteor_capacity()
            if event.type == SPAWN_METEORS:
                game.spawn_meteor()

        # gameover and new game
        if game.gameover:
            game.show_gameover_screen()
            game.__init__()

        screen.blit(background, background_rect) # displaying the background

        game.run()
        pygame.display.flip()
        clock.tick(60)