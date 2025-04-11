import serial
import time
import datetime
import json
import redis
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation

r = redis.Redis(host='localhost', port=6379, db=0)
DWM = serial.Serial(port="COM11", baudrate=115200)
print("Connected to " + DWM.name)
try:
    x = np.empty(100)
    y = np.empty(100)
    z = np.empty(100)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlim(0,8500)
    ax.set_ylim(0, 8000)
    ax.set_zlim(0, 2500)
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    ax.set_zlabel('z (mm)')
    t1, = points, = ax.plot(0, 0, 0, '*')
    a1, = ax.plot(0,0,2500,'.r')
    a2, = ax.plot(0,8000,2500,'.r')
    a3, = ax.plot(8500,0,2500,'.r')
    a4, = ax.plot(8500,8000,2500,'.r')
    a1.set_label('Anchors')
    t1.set_label('Tag')
    plt.legend(handles = [t1, a1])
    txt = fig.suptitle('')
    for q in range (100):
        data = DWM.readline()
        if(data):
            if (b"DIST" in data and b"AN0" in data and b"AN1" in data and b"AN2" in data):
                if(b"POS" in data):
                    s = ""
                    data = data.decode()
                    boo = 0
                    for i in range(len(data) - 23):
                        if (boo == 1):
                            print(data[i], end = "")
                            s = s + "" + data[i]
                        if(data[i] == ']' and boo == 1):
                            boo = 0
                            print()
                        if (data[i] == 'P' and data[i+1] == 'O' and data[i+2] == 'S'):
                            print(data[i], end = "")
                            boo = 1   
                            s = s + "" + data[i]   
                            #print("String: " + s)
                    s = s[5:len(s) - 1]
                    coord = s.split(',')
                    
                    x[q] = int(coord[0])
                    y[q] = int(coord[1])
                    z[q] = int(coord[2])
    def update_points(num, x, y, z, points):
        txt.set_text('Tag Location Sample #{:d}'.format(num)) # for debug purposes

        # calculate the new sets of coordinates here. The resulting arrays should have the same shape
        # as the original x,y,z
        new_x = x[num]
        new_y = y[num]
        new_z = z[num]
        # update properties
        points.set_data(new_x,new_y)
        points.set_3d_properties(new_z, 'z')
        # return modified artists
        return points,txt,
    ani=animation.FuncAnimation(fig, update_points, frames=100, fargs=(x, y, z, points))
    plt.show()    
    
except KeyboardInterrupt:
    print("Stop")
    DWM.write("\r".encode())
    DWM.close()
