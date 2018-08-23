def sample(file):
    jpeg = pexif.JpegFile.fromFile(file)
    cord = jpeg.get_geo()
    lat = cord[0]
    long = cord[1]
    print os.path.basename(file)

    for k in range(0, num_shp):
        if min_lat[k] < lat and max_lat[k] > lat and min_long[k] < long and max_long[k] > long:
            print(str(len(os.path.basename(file))) + str('Moving To ROI : ' + str(k)))
            directory = location + '/ROI_' + str(k)
            if not os.path.exists(directory):
                os.makedirs(directory)
            shutil.copy(file, directory)


import os
import pexif
import shutil
import shapefile
import numpy as np
import Tkinter
import Tkconstants
import tkFileDialog
from Tkinter import *
import multiprocessing as mp
from multiprocessing import Pool

# Creating root from Tkinter
root = Tk()

# Asking for input directories
location = tkFileDialog.askdirectory(
    initialdir="/", title="Select photos location")
file_shp = tkFileDialog.askopenfilename(
    initialdir="/", title="Select file", filetypes=(("shp files", "*.shp"), ("all files", "*.*")))


#files = os.listdir(location)
file = []

# listing JPG and jpg files from location
for f in os.listdir(location):
    if f.endswith('.jpg'):
        file.append(os.path.join(location, f))

    if f.endswith('.JPG'):
        file.append(os.path.join(location, f))

# reading shapefile as sf
sf = shapefile.Reader(file_shp)

# Number of shape from shapefile
shape = sf.shapes()
num_shp = len(shape)

# initializing bounding boxes
length = np.zeros((num_shp, 1))
min_long = np.zeros_like(length)
max_long = np.zeros_like(length)
min_lat = np.zeros_like(length)
max_lat = np.zeros_like(length)

# iterating over number of shapes
for i in range(0, num_shp):
    coord_1 = shape[i].points
    coord_1 = coord_1[:-1]
    length = len(coord_1)
    x = np.zeros((length, 2))
    
    # num of coordinates in shapes
    for j in range(0, length):
        coord = coord_1[j]
        x[j, 0] = coord[0]
        x[j, 1] = coord[1]

    # extering bounding box values
    min_long[i] = min(x[:, 0])
    max_long[i] = max(x[:, 0])
    min_lat[i] = min(x[:, 1])
    max_lat[i] = max(x[:, 1])

if __name__ == '__main__':
    p = Pool(mp.cpu_count())
    p.map(sample, file)
