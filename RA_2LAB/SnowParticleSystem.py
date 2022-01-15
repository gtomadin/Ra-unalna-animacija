import random
from pyglet.gl import *
import numpy as np

class SnowParticle:
    def __init__(self, position):

        self.lifeSpan = random.randrange(300, 350)

        self.position = position.copy()

        defaultSize = 25
        deltaSize = 5

        self.size = random.randrange(defaultSize - deltaSize, defaultSize + deltaSize)

        xVelocity = random.randrange(-2, 5)
        yVelocity = random.randrange(-15, -10)
        zVelocity = random.randrange(0, 1)

        self.velocity = [xVelocity, yVelocity, zVelocity]

    def update(self, deltaT):
        for i in range(0, 3):
            self.position[i] = self.position[i] + self.velocity[i] * deltaT * 60
        #self.size = self.size + deltaT * 10;
        self.lifeSpan = self.lifeSpan - deltaT * 60


class SnowParticleSystem:
    def __init__(self):
        self.particles = []
        self.texture = pyglet.image.load("snow.bmp").get_texture()
        self.numberOfParticles = 500
        #self.timer = 0

        self.createNewParticles()

    def createNewParticles(self):

        xPosition = random.randrange(-3500, 3500)
        yPosition = random.randrange(2500, 2600)
        zPosition = random.randrange(0, 1)

        particle = SnowParticle(np.array([xPosition, yPosition, zPosition]))
        self.particles.append(particle)


    def update(self, deltaT):

        #self.timer = self.timer + deltaT * 60

        for particle in self.particles:
            particle.update(deltaT)


            if particle.lifeSpan <= 0:
                self.particles.remove(particle)

        if len(self.particles) <  self.numberOfParticles:
            self.createNewParticles()


    def draw(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPushMatrix()

        for particle in self.particles:

            ##https://gist.github.com/vanne02135/305997/a403f5b60ab50c1fb756f3a5e88122afdd7ee79d
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex3f(particle.position[0] - particle.size, particle.position[1] - particle.size, particle.position[2])
            glTexCoord2f(1, 0)
            glVertex3f(particle.position[0] + particle.size, particle.position[1] - particle.size, particle.position[2])
            glTexCoord2f(1, 1)
            glVertex3f(particle.position[0] + particle.size, particle.position[1] + particle.size, particle.position[2])
            glTexCoord2f(0, 1)
            glVertex3f(particle.position[0] - particle.size, particle.position[1] + particle.size, particle.position[2])


            glEnd()


        glPopMatrix()
        glDisable(self.texture.target)