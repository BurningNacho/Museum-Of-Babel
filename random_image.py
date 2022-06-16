from PIL import Image, ImageTk
import numpy as np
from time import sleep

WIDTH = 256
HEIGHT = 256


'''
    Generates a random RGB Image of size width*height
'''
def random_img(width, height):
    array = np.random.randint(0,255, (height,width,3))
    array = np.array(array, dtype=np.uint8)
    # estimate_noise(array)
    img = Image.fromarray(array)
    return img


'''
    Generates the next RGB Image of size width*height
'''
## Using sample image
im = Image.open('281379.jpg')
# im = random_img(WIDTH, HEIGHT)
counter_array = np.asarray(im, dtype=np.uint8)
#

# counter_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
# counter_array = np.array(counter_array)
def next_img(width, height):
    global counter_array
    # print(counter_array)
    counter_array = get_next_array(counter_array, 0, 0, 0)
    img = Image.fromarray(counter_array)
    return img

def get_next_array(counter_array, i, j, k):
    print(f'i:{i} j:{j} k:{k} RGB:{counter_array[i][j]}')
    # SII Estamos en el ultimo color RGB (Blue)
    if k == 3:
        return get_next_array(counter_array, i, j + 1, 0)

    # SII Estamos en el ultimo pixel de la fila
    if j == WIDTH:
        return get_next_array(counter_array, i + 1, 0, 0)
    if i == HEIGHT:
        return counter_array

    # SII Estamos en el ultimo valor RGB (255)
    if counter_array[i][j][k] >= 255 - 85:
        counter_array[i][j][k] = 0
        return get_next_array(counter_array, i, j, k + 1)
    else:
        counter_array[i][j][k] += 85

    return counter_array
    # return np.array(counter_array, dtype=np.uint8)

""" Estimate the RMS noise of an image

from http://stackoverflow.com/questions/2440504/
noise-estimation-noise-measurement-in-image

Reference: J. Immerkaer, “Fast Noise Variance Estimation”,
Computer Vision and Image Understanding,
Vol. 64, No. 2, pp. 300-302, Sep. 1996 [PDF]

"""
def estimate_noise(data):

    H, W = data.shape

    data = np.nan_to_num(data)

    M = [[1, -2, 1],
         [-2, 4, -2],
         [1, -2, 1]]

    sigma = np.sum(np.sum(np.abs(convolve2d(data, M))))
    sigma = sigma * np.sqrt(0.5 * np.pi) / (6 * (W - 2) * (H - 2))

    return sigma

'''This will simply generate a new image every X units of time and
try to display it. If the file is not an image then it will be skipped.
Click on the image display window to go to the next image.

Noah Spurrier 2007'''
import os, sys
import tkinter

# def button_click_exit_mainloop (event):
#     event.widget.quit() # this will cause mainloop to unblock.

# root.bind("<Button>", button_click_exit_mainloop)
old_label_image = None
def Refresher():
    try:
        # image1 = random_img(256, 256)
        image1 = next_img(WIDTH, HEIGHT)
        # print(image1)
        image1.save('tst.png')
        # image1.show()
        root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = tkinter.Label(root, image=tkpi)
        label_image.pack()
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
        if old_label_image is not None:
            old_label_image.destroy()
        old_label_image = label_image
    except Exception as e:
        # This is used to skip anything not an image.
        # Warning, this will hide other errors as well.
        pass
    root.after(1, Refresher)

root = tkinter.Tk()
root.geometry('+%d+%d' % (WIDTH, HEIGHT))
Refresher()
root.mainloop() # wait until user clicks the window

# random_img('random.png', 1024, 1024)
