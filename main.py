from PIL import Image
import numpy as np
from numpy import asarray
from sympy import im
import os, glob
import time

def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def slice_image(path, width, height, frame_num, grid_count):
    """
    Function to split the image at the given location into width*height amount of pieces

    path -> path to the image location
    width -> number of width slices you want cut
    height -> number of height slices you want cut
    """

    start_num=0+frame_num*grid_count
    width=width//8
    height=height//8
    for k,piece in enumerate(crop(path,height,width),start_num):
        img=Image.new('RGB', (width, height), 255)
        img.paste(piece)
        path=os.path.join(f'images/sliced-image/{k}.png')
        img.save(path)


def split_gif(path, size):
    gif = Image.open(path)
    num_frames = gif.n_frames

    for i in range(num_frames):
        gif.seek(i)
        gif.resize(size=size)
        gif.save(f'images/sliced-gif/{i}.png')

    #gif.close()

    return num_frames


def clear_current():
    dir = 'images/sliced-gif'
    for file in os.scandir(dir):
        os.remove(file.path)
    dir = 'images/sliced-image'
    for file in os.scandir(dir):
        os.remove(file.path)
    dir = 'images/stitched-images'
    for file in os.scandir(dir):
        os.remove(file.path)


def stitch_images(num_frames, grid_count):
    for i in range(grid_count):
        related_images = []
        for n in range(num_frames):
            related_images.append(Image.open(f'images/sliced-image/{i+(n*grid_count)}.png'))
        combined = np.concatenate(related_images, axis=0)
        Image.fromarray(combined).save(f'images/stitched-images/{i}.png')


def create_images(path, size):
    
    clear_current()

    num_frames = split_gif(path, size)

    for i in range(num_frames):
        slice_image(f'images/sliced-gif/{i}.png', size[0], size[1], i, (size[0]//16)*(size[1]//16))
    
    #time.sleep(3)

    stitch_images(num_frames, (size[0]//16)*(size[1]//16))


def create_animation_files(path, size):
    if size[0]%16 != 0 or size[1]%16 != 0: 
        print("Size dimensions must be a multiple of 16")
        return ''

    create_images(path, size)
    grid_count = (size[0]//16)*(size[1]//16)

    for i in range(grid_count):
        f = open(f'images/stitched-images/{i}.png.mcmeta', 'w')
        f.write(
            """
            {
                "animation": {
                    "frametime": 2
                }
            }
            """)







create_animation_files('images/HEHEHEHA.gif', (128, 128))

#split_gif('images/HEHEHEHA.gif', (128,128))
#slice_image('images/HEHEHEHA-scaled.PNG', 8, 8)