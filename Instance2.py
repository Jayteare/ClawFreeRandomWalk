import numpy as np
import math
import collections
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import paho.mqtt.subscribe as subscribe
import random

matrix_x = 10
matrix_y = 100
matrix = np.random.rand(2)
def Gen_RandLine(choice):
    
    if choice == 0:
        #Generated Matrix of 0 to 1 bits
        matrix_x = 10
        matrix_y = 100
        matrix = np.random.randint(5,size=(matrix_x,matrix_y))
        for i in range(len(matrix)):
            step = np.random.randint(2,size=1) + random.choice([-0.5,0.5]) + np.random.randint(50)*0.3
            step = step * 1.2
            matrix[i] = matrix[i] + (step * random.choice([+0.10,+0.15]))
            matrix[i] = matrix[i] + random.choice([-1,1])
    elif choice == 1:
        #Generated Matrix of 0 to 1 bits
        matrix_x = 10
        matrix_y = 100
        matrix = np.random.randint(5,size=(matrix_x,matrix_y))
        for i in range(len(matrix)):
            step = np.random.randint(5,size=1) + random.choice([-0.5,0.5]) + np.random.randint(50)*0.3
            step = step * 0.8
            matrix[i] = matrix[i] + (step * random.choice([-0.10,+0.10]))
            matrix[i] = matrix[i] + random.choice([-0.5,1])
        
    return matrix


def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
    return lines

msg = subscribe.simple("data/matrix", hostname="localhost")
print("%s %s" % (msg.topic, msg.payload))

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines
data = [Gen_RandLine(int(msg.payload)) for index in range(50)]

# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

# Setting the axes properties
ax.set_xlim3d([0.0, 10.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 10.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 10.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
                                   interval=50, blit=False)

plt.show()
