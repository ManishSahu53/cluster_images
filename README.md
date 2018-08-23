# cluster-image

## Introduction
This program will cluster images according to shape file provided. Currently bounding box is used to mark areas from shape files

## Dependencies
1. shutil
2. pyshp
3. multiprocessing
4. pexif

To install dependencies type
```
pip install shutil
pip install pyshp
pip install multiprocessing
```
To install pexif, download pexif from this [link](https://github.com/mcbridejc/pexif.git) as zip and extract it to pexif folder.

If pexif is extract in *C:/Downloads* then run
```
cd C:/Downloads/pexif
python setup.py build
python setup.py install
```

If you have git then type
```
git clone https://github.com/mcbridejc/pexif.git pexif
cd pexif
python setup.py build
python setup.py install
```

# How to run
To run this
1. Open cmd (command prompt) or terminal and type 
```
python cluster_im.py
```
2. Provide folder containing images
3. Provide shapefile using which images are to be clustered.

**Note** - Shapefiles must in Geographic coordinate system WGS84 and not UTM/Projected coordinate system. 