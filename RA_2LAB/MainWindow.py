from pyglet.gl import *
from pyglet.window import *

from FireworkParticleSystem import FireworkParticleSystem
from SnowParticleSystem import SnowParticleSystem

window = pyglet.window.Window(width=800, height=650)


FireworkParticleSystem = FireworkParticleSystem()
SnowParticleSystem = SnowParticleSystem()

@window.event
def on_draw():

    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(50, window.width/window.height, 0.05, 10000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    gluLookAt(0, 0, 6000, 0, 0, 0, 0, 1.0, 0)

    glPushMatrix()
    FireworkParticleSystem.draw()
    SnowParticleSystem.draw()
    glPopMatrix()
    glFlush()


# azuriranje timera
def update(deltaT):
   FireworkParticleSystem.update(deltaT)
   SnowParticleSystem.update(deltaT)

# pokretanje applikacije

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()

