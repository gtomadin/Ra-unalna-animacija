from pyglet.gl import *
from pyglet.window import *
import numpy as np
import ctypes

file_name = "kocka.obj"
spline_file = "bspline.txt"
rot ="dcm"

Points = [] #tocke objekta
Poligons = [] #poligonni objekta

Spline_Points = [] # tocke krivulje

Spline_Segments = [] # segmenti krivulje
Spline_Tangent = [] # tangente krivulje

Spline_Second_Diff = [] # druge derivacije krivulje

NumberOfT = 30 # broj intervala
Time = np.linspace(0,1,NumberOfT) # intervali
timer = 0 # timer
B_i3 = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) # periodički segment kubne B-krivulje
B_i3d = np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]]) # periodički segment kubne B-krivulje za prvu derivaciju
B_i3d2 = np.array([[-1, 3, -3, 1], [2, -4, 2, 0]]) # periodički segment kubne B-krivulje za drugu derivaciju

# citanje objekta iz file 4. IRG labos
def reading_file(file_name):
    global Points, Poligons

    file = open(file_name)

    for line in file:
        if line.startswith("v"):
            elem = line.split()
            Points.append((float(elem[1]), float(elem[2]), float(elem[3])))
        if line.startswith("f"):
            elem = line.split()
            Poligons.append((int(elem[1]) - 1, int(elem[2]) - 1, int(elem[3]) - 1))

# citanje krivulje iz file 4. IRG labos
def reading_spline(spline_file):
    global Spline_Points

    file = open(spline_file)

    for line in file:
        if line.startswith("v"):
            elem = line.split()
            Spline_Points.append((float(elem[1]), float(elem[2]), float(elem[3])))

# crtanje obijekta 4. IRG labos
def drawObject():
    global Points, Poligons

    reading_file(file_name)

    glBegin(GL_LINES)

    for poligon in Poligons:
        Point_1 = Points[poligon[0]]
        Point_2 = Points[poligon[1]]
        Point_3 = Points[poligon[2]]

        #print(V1)
        #print(V2)
        #print(V3)

        glVertex3f(Point_1[0], Point_1[1], Point_1[2])
        glVertex3f(Point_2[0], Point_2[1], Point_2[2])

        glVertex3f(Point_2[0], Point_2[1], Point_2[2])
        glVertex3f(Point_3[0], Point_3[1], Point_3[2])

        glVertex3f(Point_3[0], Point_3[1], Point_3[2])
        glVertex3f(Point_1[0], Point_1[1], Point_1[2])


    glEnd()

# crtanje b-krivulje i tangenti
def draw_bspline_and_tangents():
    global Spline_Points
    global Spline_Segments
    global Spline_Tangent

    # crtanje b-krivulje
    glBegin(GL_LINE_STRIP)
    for segment_index in range(0, len(Spline_Segments) - 1):
        glColor3f(0, 0, 0)
        #print(Spline_Segments[segment_index])
        glVertex3f(Spline_Segments[segment_index][0] ,Spline_Segments[segment_index][1], Spline_Segments[segment_index][2])
        glVertex3f(Spline_Segments[segment_index+1][0], Spline_Segments[segment_index+1][1], Spline_Segments[segment_index+1][2])
    glEnd()


    tang_C = [] #skup skaliranih tangenti
    scala = 0.1

    # skaliranje tangenti
    for tangent_index in range(len(Spline_Tangent)):

        x = (Spline_Segments[tangent_index][0] + Spline_Tangent[tangent_index][0])/2
        y = (Spline_Segments[tangent_index][1] + Spline_Tangent[tangent_index][1])/2
        z = (Spline_Segments[tangent_index][2] + Spline_Tangent[tangent_index][2])/2

        x = scala * x + Spline_Segments[tangent_index][0]
        y = scala * y + Spline_Segments[tangent_index][1]
        z = scala * z + Spline_Segments[tangent_index][2]

        A = np.array([x, y, z])
        tang_C.append(A)

    # crtanje tangenti b-krivulje
    glBegin(GL_LINES)
    for tangent_index in range(0, len(tang_C) - 1, 2):
        glColor3f(0, 1, 0)
        glVertex3f(Spline_Segments[tangent_index][0], Spline_Segments[tangent_index][1], Spline_Segments[tangent_index][2])
        glVertex3f(tang_C[tangent_index][0], tang_C[tangent_index][1], tang_C[tangent_index][2])
    glEnd()

# odredivanje osi rotacije i kut rotacije
def rotation(s, e):
    rotation_axis = np.cross(s, e) # vektorski produkt vektora s i e - os rotacije

    # racunanje kuta rotacije
    angle = np.matmul(s, e)
    s_norm = pow((s[0] ** 2 + s[1] ** 2 + s[2] ** 2), 1 / 2) # norma s
    e_norm = pow((e[0] ** 2 + e[1] ** 2 + e[2] ** 2), 1 / 2) # norma e

    rotation_angle = np.rad2deg(np.arccos(angle / (s_norm * e_norm))) # kut rotacije

    return rotation_angle, rotation_axis

# Rotacijska matrica, DCM rotacija
def rotationDCM(pt_dev1, pt_dev2):
    pt_dev1 = pt_dev1 / np.linalg.norm(pt_dev1) # normiramo prvu derivaciju - tangentu
    pt_dev2 = pt_dev2 / np.linalg.norm(pt_dev2) # normitamo drugu derivaciju
    all_zeros = not np.any(pt_dev2) # provijera ima li druga derivacija 0 https://stackoverflow.com/questions/18395725/test-if-numpy-array-contains-only-zeros

    if all_zeros:
        u = pt_dev1 # ako ima uzimamo tangentu
    else:
        u = np.cross(pt_dev1, pt_dev2) # ako nema uzimamo vektorski umnozak drve i druge derivacije

    w = pt_dev1
    v = np.cross(w, u)
    help = [[w[0], u[0], v[0], 0], [w[1], u[1], v[1], 0], [w[2], u[2], v[2], 0], [0, 0, 0, 1]] # stvaranje matrice rotacije

    R = np.array(help) # matrica rotacije
    R_inv = np.linalg.inv(R) # inverz matrice rotacije
    return R_inv

reading_spline(spline_file)
#print(Spline_Points)

# izracun svih tocaka
numberOfSegments = len(Spline_Points) - 3 # broj segemanta jednak je broju točaka - 3


for segment_index in range(numberOfSegments):

    # 4 točke svakog segmenta
    r_0 = Spline_Points[segment_index]
    r_1 = Spline_Points[segment_index + 1]
    r_2 = Spline_Points[segment_index + 2]
    r_3 = Spline_Points[segment_index + 3]

    R_i = np.array([r_0, r_1, r_2, r_3])

    # za svaki t se izračunava
    for t in Time:
        #print(t)

        # Izračun segmenta

        T_3 = np.array([t**3, t**2, t, 1])
        #print(T_3)
        T_36 = T_3 / 6.
        #print(T_36)
        T_36_B_i3 = np.matmul(T_36, B_i3)
        #print(T_36_B_i3)
        T_36_B_i3_R_i = np.matmul(T_36_B_i3, R_i)
        #print(T_36_B_i3_R_i)
        Spline_Segments.append(T_36_B_i3_R_i)


        # Izračun tangente

        T_2 = np.array([t**2, t, 1])
        #print(T_2)
        T_22 = T_2 / 2.
        #print(T_22)
        T_22_B_i3d = np.matmul(T_22, B_i3d)
        #print(T_22_B_i3d)
        T_22_B_i3d_R_i = np.matmul(T_22_B_i3d, R_i)
        #print(T_22_B_i3d_R_i)
        Spline_Tangent.append(T_22_B_i3d_R_i)


        #Izračun druge derivacije

        T_sec_diff = np.array([2 * t, 1])
        T_sec_diff2 = T_sec_diff / 2.
        T_sec_diff2_B_i3d2 = np.matmul(T_sec_diff2, B_i3d2)
        T_sec_diff_B_i3d2_R_i = np.matmul(T_sec_diff2_B_i3d2, R_i)
        Spline_Second_Diff.append(T_sec_diff_B_i3d2_R_i)




window = pyglet.window.Window()

# Promjena velicine prozora 4. labos
@window.event
def on_resize(new_width, new_height):
    glViewport(0, 0, new_width, new_height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    #glClear(GL_COLOR_BUFFER_BIT)
    gluPerspective(30, 1, 1, 0)
    #glColor3f(0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


# crtanje elemenata
@window.event
def on_draw():
    global timer

    window.clear()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-10, 0, -120.0)
    glRotatef(25, 0, 1, 0)


    print(timer)

    glColor3f(0, 0, 0)
    draw_bspline_and_tangents()

    # crtanje b- krivulje za svaku točku
    current_point = Spline_Segments[timer]
    current_tangent = Spline_Tangent[timer]
    current_second_dev = Spline_Second_Diff[timer]

    if rot == "dcm":
        R_inv = rotationDCM(current_tangent, current_second_dev)
        newpoint = np.array([current_point[0], current_point[1], current_point[2], 0])
        #print(newpoint)
        #print(R_inv)
        R_inv_point = np.dot(newpoint, R_inv)
        #print(R_inv_point)
        #glTranslatef(R_inv_point[0], R_inv_point[1], R_inv_point[2])

        # promjena orijentacije x, y, z u w, u, v
        # https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glMultMatrix.xml
        help = []
        for i in range(4):
            for j in range(4):
                help.append(R_inv[i][j])
        help = (ctypes.c_float * len(help))(*help)
        glTranslatef(current_point[0], current_point[1], current_point[2])
        glMultMatrixf(help)
        #print(help)

    else:
        # promjena orijentacije pomocu osi rotacije i kuta rotacije
        s = [0, 0, 1]
        #glPushMatrix()
        glTranslatef(current_point[0], current_point[1], current_point[2])
        rotation_angle, rotation_axis = rotation(s, current_tangent)
        glRotatef(rotation_angle, rotation_axis[0], rotation_axis[1], rotation_axis[2])
        #glPopMatrix()

    # crtanje objekta
    glColor3f(1, 0, 0)
    drawObject()



    glFlush()



# azuriranje timera
def update(arg):
    global timer
    timer = timer + 1
    if timer >= len(Spline_Segments):
        timer = 0

# pokretanje applikacije
pyglet.clock.schedule(update)
pyglet.app.run()