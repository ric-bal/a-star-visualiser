import os
from numpy import * 
import cv2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
check_array = array([100, 100, 100]) # increase all array values for more leniency

# GETTING IMAGE FILE
folder = 'Image\\'
file = os.listdir(folder)[0]  # first file in folder
file_path = os.path.join(folder, file)

img = cv2.imread(file_path)


def set_width(WIDTH):
    #pass
    global img
    img = cv2.resize(img, (WIDTH, WIDTH))
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyWindow('image')


def get_pixel_colour(y, x):
    img_pixel = array(img[x][y], int)
    if not False in (img_pixel <= check_array): 
        return BLACK
    else:
        return WHITE






"""
a = array([1,2,3,0]) 
b = array([0,2,3,1]) 
c = a == b 
print('Result of a==b:', c) 
c = a > b 
print('Result of a>b:', c) 
c = a <= b 
print('Result of a<=b:', c)
"""
                        