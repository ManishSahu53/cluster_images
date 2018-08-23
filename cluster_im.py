"""Cluster images from shape file"""

# Clustering images
def cluster(file):
    count = len(file)
    f = open(file, 'rb')
    jpeg = pexif.JpegFile.fromFile(file)
    cord = jpeg.get_geo()
    lat = cord[0]
    long = cord[1]
    print file

    for k in range(0, num_shp):
        if min_lat[k] < lat and max_lat[k] > lat and min_long[k] < long and max_long[k] > long:
            print(str(file) + str(' moving To ROI_: ' + str(k)))
            directory = os.path.join(location, 'ROI_' + str(k))
            if not os.path.exists(directory):
                os.makedirs(directory)
            shutil.copy(file, directory)

# Importing libraries

import os
import sys
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

# Defining root in Tkinter
root = Tk()

# Ask for input folder and shape files
location = tkFileDialog.askdirectory(
    initialdir="/", title="Select photos location")
shp_file = tkFileDialog.askopenfilename(
    initialdir="/", title="Select file", filetypes=(("shp files", "*.shp"), ("all files", "*.*")))

# Reading shapefiles
sf = shapefile.Reader(shp_file)

# Extracting number of shapes
shapes = sf.shapes()
num_shp = len(shapes)

# Initializing variables
length = np.zeros((num_shp, 1))
print('%s shapes found' % (str(length)))

min_long = np.zeros_like(length)
max_long = np.zeros_like(length)
min_lat = np.zeros_like(length)
max_lat = np.zeros_like(length)
files = []
status = 0

# Listing files inside location folder
for _, _, filename in os.walk(location):
    for file in filename:
        fileExt = os.path.splitext(file)[-1]
        if fileExt == '.jpg':
            files.append(os.path.join(location, file))

        if fileExt == '.JPG':
            files.append(os.path.join(location, file))

if len(files) < 1:
    sys.exit('No images were found in %s location' % (location))

# Extracting bounding boxes
for i in range(0, num_shp):
    coord = shapes[i].points
    coord = coord[:-1]
    length = len(coord)
    x = np.zeros((length, 2))
    for j in range(0, length):
        coord = coord[j]
        x[j, 0] = coord[0]
        x[j, 1] = coord[1]
    min_long[i] = min(x[:, 0])
    max_long[i] = max(x[:, 0])
    min_lat[i] = min(x[:, 1])
    max_lat[i] = max(x[:, 1])

    if max_lat[i] > 200:
        sys.exit('Input shape file must be in geographic coordinate system WGS84')

# Main program for multi processing
if __name__ == '__main__':
    p = Pool(mp.cpu_count())
    print(p.imap(cluster, files))
