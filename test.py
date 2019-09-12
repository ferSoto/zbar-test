#!/usr/bin/env python

# python test.py {folder with images}

import cv2
import json
import numpy as np
import os
import sys
import zbar

def normalize(image):
    height, width = image.shape
    normalized = np.zeros((height, width), dtype=np.uint8)
    cv2.normalize(image, normalized, 0, 255, cv2.NORM_MINMAX)
    return normalized

def threshold(image):
    return cv2.threshold(image,127,255,cv2.THRESH_BINARY)[1]

def adaptiveThreshold(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

def sharpening(image):
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])

    sharpened = cv2.filter2D(image, -1, kernel_sharpening)
    return sharpened

def scan_image(image):
    scanner = zbar.Scanner()
    results = scanner.scan(image)

    for result in results:
        return str(result.data)

def prints(text, _str):
    print(text + (_str if _str is not None else 'Not fount'))

def show(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)

if len(sys.argv) != 2:
    print('Argument missing...')
    exit(1)

folder = sys.argv[1]
if not os.path.exists(folder):
    print('Directory does not exists...')
    exit(2)

files = os.listdir(folder)
files = sorted(files)
if len(files) == 0:
    print('Folder without files...')
    exit(3)

for file in files:
    _, ext = os.path.splitext(file)
    if ext not in ('.jpg', '.jpeg', '.png'):
        continue
    print(file)
    path = folder + '/' + file
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    #show(image)
    #result = scan_image(image)
    #prints('No preprocessing -> ', result)
    image = normalize(image)
    #show(image)
    result = scan_image(image)
    prints('', result)
    #image = adaptiveThreshold(image)
    #show(image)
    #result = scan_image(image)
    #prints('Adaptive Gaussian Threshold -> ', result)
    print(" ")
