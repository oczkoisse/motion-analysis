import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

import matplotlib.animation as animation

import itertools

from mpl_toolkits.mplot3d import Axes3Dimport numpy as npkinect_lines = [ #head

                   [3,2,20],

                   # Left arm

                   [20, 4, 5, 6],

                   #Left hand

                   [22, 6, 7, 21],

                   #Right hand

                   [24, 10, 11, 23],

                   # Right arm

                   [10, 9, 8, 20],

                   # Torso

                   [20, 1, 0],

                   # Left leg

                   [0, 12, 13, 14,15],

                   # Right leg

                   [0, 16, 17 ,18 , 19]]

#kinect_lines = kinect_lines[5:6]pause = False

frame = 0
def vis_skeleton(sks, kinect_version = 2, interval = 25, color = None, fig=None, repeat=True):

   #animation based visualization, much faster than the naive frame-by-frame plot

   print sks[0].shape    if fig:

       fig = plt.figure(fig)

   else:

       fig = plt.figure()

   ax = fig.add_subplot(111, projection='3d')    ax.set_xlim(-1, 1)

   ax.set_ylim(1.5, 3.5)

   ax.set_zlim(-1,  1)    ax.set_xlabel('X')

   ax.set_ylabel('Z')

   ax.set_zlabel('Y')    ax.set_title('Skeleton Display')    lines = [ax.plot([0]*2, [0]*2, [0]*2 )  for l in kinect_lines]    def update_draw(sk, lines, kinect_lines):

       a = sk.reshape((-1,3))

       print a.shape

       print a

       for line, limb in zip(lines, kinect_lines):

           print a[limb][:,[0,2]].T

           line[0].set_data(a[limb][:,[0,2]].T)

           line[0].set_3d_properties(a[limb][:,1])

           line[0].set_marker('o')

           if color is not None:

               line[0].set_color(color)

       print "="*10    line_ani = animation.FuncAnimation(fig, update_draw, sks, fargs=(lines, kinect_lines), interval=interval, repeat=False)

   plt.show(block=False)

   plt.close("all")

   #line_ani.save("../Files/kinect.mp4",fps=30,writer=animation.FFMpegFileWriter())
