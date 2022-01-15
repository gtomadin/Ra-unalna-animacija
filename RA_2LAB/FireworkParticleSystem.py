import random
from pyglet.gl import *
import numpy as np


class FireworkParticle:
    def __init__(self, position):

        self.lifeSpan = random.randrange(20, 40)

        self.position = position.copy()

        defaultSize = 50
        deltaSize = 25

        self.size = random.randrange(defaultSize - deltaSize, defaultSize + deltaSize)


        xVelocity = random.randrange(-20, 20)
        yVelocity = random.randrange(-20, 20)
        zVelocity = random.randrange(-5, 5)

        if (abs(xVelocity) > 17 or abs(yVelocity) > 17):
            self.lifeTime = 70

        if (abs(xVelocity) > 10 and abs(yVelocity) > 10):
            if xVelocity > 0:
                xVelocity = xVelocity - 5
            if yVelocity > 0:
                yVelocity = yVelocity - 5
            if xVelocity < 0:
                xVelocity = xVelocity + 5
            if yVelocity < 0:
                yVelocity = yVelocity - 5

        self.velocity = [xVelocity, yVelocity, zVelocity]

    def update(self, deltaT):
        for i in range(0 ,3):
            self.position[i] = self.position[i] + self.velocity[i] * deltaT * 60

        self.lifeSpan =  self.lifeSpan - deltaT * 60


class FireworkParticleSystem:
    def __init__(self):
        self.particles = []
        #https://www.geeksforgeeks.org/pyglet-loading-texture/
        self.texture = pyglet.image.load("cestica.bmp").get_texture()
        self.numberOfParticles = 100
        self.timer = 0

        self.createNewParticles()

    def createNewParticles(self):

        xPosition = random.randrange(-1250, 1250)
        yPosition = random.randrange(-1250, 1250)
        zPosition = random.randrange(-1250, 1250)

        for i in range(0, self.numberOfParticles):
            particle = FireworkParticle(np.array([xPosition, yPosition, zPosition]))
            self.particles.append(particle)


    def update(self, deltaT):

        self.timer = self.timer + deltaT * 60

        for particle in self.particles:
            particle.update(deltaT)
            if particle.lifeSpan <= 0:
                self.particles.remove(particle)

        if self.timer > 50:
            self.timer = 0
            self.numberOfParticles = random.randint(100, 125)
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