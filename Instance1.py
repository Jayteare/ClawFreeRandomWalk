from mpi4py import MPI
import numpy as np
import math
import collections
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import random
import paho.mqtt.client as mqtt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# passing MPI datatypes explicitly
if rank == 0:
    #Generated Matrix of 0 to 1 bits
    matrix_x = 10
    matrix_y = 100
    matrix = np.random.rand(2)

    def Gen_RandLine():
        choice = random.choice([0,1])
        if choice == 0:
            #Generated Matrix of 0 to 1 bits
            matrix_x = 10
            matrix_y = 100
            matrix = np.random.randint(5,size=(matrix_x,matrix_y))
            for i in range(len(matrix)):
                #
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

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # Fifty lines of random 3-D lines
    data = [Gen_RandLine() for index in range(50)]

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

    ax.set_title('CLUSTER 1')

    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
                                       interval=50, blit=False)

    plt.show()
    pass_choice = random.choice([0,1])
    broker_address="localhost"
    port=1883
    client = mqtt.Client("Instance1") #create new instance
    client.connect(broker_address,port) #connect to broker
    client.publish("data/matrix",pass_choice)#publish
    comm.Send([matrix, MPI.INT], dest=1, tag=77)
    
elif rank == 1:
    matrix_x = 10
    matrix_y = 100
    matrix = np.random.randint(2,size=(matrix_x,matrix_y))
    claw = np.random.randint(2,size=(matrix_x,matrix_y))
    comm.Recv([matrix, MPI.INT], source=0, tag=77)

    bit_e = 0
    bit_n = 0
    ravel_matrix = matrix.ravel()
    ravel_claw = claw.ravel()

    for i in range(len(ravel_matrix)):
      if ravel_matrix[i] == ravel_claw[i]:
        bit_e = bit_e + 1
      elif ravel_matrix[i] != ravel_claw[i]:
        bit_n = bit_n + 1

    print("Equal: " + str(bit_e))
    print("Not Equal: " + str(bit_n))

    def Gen_RandLine():
        #Generated Matrix of 0 to 1 bits
        matrix_x = 10
        matrix_y = 100
        matrix = np.random.randint(2,size=(matrix_x,matrix_y))
        for i in range(len(matrix)):
          matrix[i] = (matrix[i]/0.2 - 1)*0.3
          step = np.random.randint(2,size=1) - 0.1
          step = step * 0.1
          matrix[i] = matrix[i] + step
        
        return matrix


    def update_lines(num, dataLines, lines):
        for line, data in zip(lines, dataLines):
            line.set_data(data[0:2, :num])
            line.set_3d_properties(data[2, :num])
        return lines

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # Fifty lines of random 3-D lines
    data = [Gen_RandLine() for index in range(50)]

    # Creating fifty line objects.
    # NOTE: Can't pass empty arrays into 3d version of plot()
    lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

    # Setting the axes properties
    ax.set_xlim3d([0.0, 1.0])
    ax.set_xlabel('X')

    ax.set_ylim3d([0.0, 1.0])
    ax.set_ylabel('Y')

    ax.set_zlim3d([0.0, 1.0])
    ax.set_zlabel('Z')

    ax.set_title('WALK 2')

    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, update_lines, 50, fargs=(data, lines),
                                       interval=50, blit=False)

    plt.show()
