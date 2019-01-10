"""Cluster images from shape file"""

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
# import multiprocessing as mp
# from multiprocessing import Pool


# Clustering images
def cluster(file):
    count = len(file)
    f = open(file, 'rb')
    jpeg = pexif.JpegFile.fromFile(file)
    cord = jpeg.get_geo()
    lat = cord[0]
    long = cord[1]

    for k in range(0, num_shp):
        if min_lat[k] < lat and max_lat[k] > lat and min_long[k] < long and max_long[k] > long:
            print(str(file) + str(' copying To ROI_: ' + str(k)))
            directory = os.path.join(os.path.dirname(file), 'ROI_' + str(k))
            if not os.path.exists(directory):
                os.makedirs(directory)
            shutil.copy(file, directory)


def main():
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
    global num_shp
    num_shp = len(shapes)

    # Initializing variables
    length = np.zeros((num_shp, 1))
    print('%s shapes found' % (str(num_shp)))

    global min_long, max_long, min_lat, max_lat

    min_long = np.zeros_like(length)
    max_long = np.zeros_like(length)
    min_lat = np.zeros_like(length)
    max_lat = np.zeros_like(length)
    files = []
    status = 0

    # Listing files inside location folder
    for root, _, filename in os.walk(location):
        for file in filename:
            fileExt = os.path.splitext(file)[-1]
            if fileExt == '.jpg':
                files.append(os.path.join(root, file))

            if fileExt == '.JPG':
                files.append(os.path.join(root, file))
    if len(files) < 1:
        sys.exit('No images were found in %s location' % (location))

    # Extracting bounding boxes
    for i in range(0, num_shp):
        coord = shapes[i].points
        coord = coord[:-1]
        length = len(coord)
        x = np.zeros((length, 2))
        for j in range(0, length):
            coord_ = coord[j]
            x[j, 0] = coord_[0]
            x[j, 1] = coord_[1]
        min_long[i] = min(x[:, 0])
        max_long[i] = max(x[:, 0])
        min_lat[i] = min(x[:, 1])
        max_lat[i] = max(x[:, 1])

        if max_lat[i] > 200:
            sys.exit('Input shape file must be in geographic coordinate system WGS84')
    
    for i in files:
        cluster(i)
    # p = Pool(mp.cpu_count())
    # p.imap(cluster, files)


# Main program for multi processing
if __name__ == '__main__':
    main()