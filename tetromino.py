import numpy as np
import random

square_shape = [
    [0,0,0,0],
    [0,1,1,0],
    [0,1,1,0],
    [0,0,0,0]
    ]

line_shape = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [1,1,1,1]
    ]

z_shape = [
    [0,0,0,0],
    [0,0,1,1],
    [0,1,1,0],
    [0,0,0,0]
    ]

t_shape = [
    [0,0,0,0],
    [0,0,1,0],
    [0,1,1,1],
    [0,0,0,0]
    ]

l_shape = [
    [0,0,0,0],
    [0,0,1,0],
    [0,0,1,0],
    [0,0,1,1]
    ]



class Tetromino:
    def __init__(self, shape, rotation):
        #self.name = name #name of shape
        self.shape = np.array(shape) #2d array of how shape looks
        self.rotation = rotation #current rotation in degrees

    def rotateCCW(self):
        self.shape = np.rot90(self.shape)
    def rotateCW(self):
        self.shape = np.rot90(self.shape, k=-1)
        
def returnRandomShape():
    shapes = [square_shape,line_shape,z_shape,t_shape,l_shape]
    return random.choice(shapes)
    #return line_shape


