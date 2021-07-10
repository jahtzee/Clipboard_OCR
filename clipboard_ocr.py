# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 19:19:17 2021

@author: jahtzee
"""

# Import
import sys
import os
#import PySimpleGUI as sg
import cv2
import pytesseract
from PIL import ImageGrab
import tempfile
import pyperclip
from infi.systray import SysTrayIcon
import numpy as np

# Definitions

languages = 'eng+ger'
custom_config = r'--oem 3 -l '+languages+' --psm 6'
temp = tempfile.gettempdir()

def saveImageFromClipboard():
    clip = ImageGrab.grabclipboard()
    try:
        clip.save(temp+'\ocr_tmp.PNG', 'PNG')
    except: 
        return 'Error'
    return temp+'\ocr_tmp.PNG'
    
def OCRImageFromTemp(path):
    if (path == 'Error'):
        return 'Error - Check clipboard contents!'
    img = cv2.imread(path)
    img = preprocessImage(img)
    string = str(pytesseract.image_to_string(img, config=custom_config))
    os.remove(temp+'\ocr_tmp.PNG')
    string = string.replace("\f","")
    string.strip()
    return string

def systrayOption(systray):
    path = saveImageFromClipboard()
    pyperclip.copy(OCRImageFromTemp(path))  

def preprocessImage(image):
    image = getGrayscale(image)
    return image

# get grayscale image
def getGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def removeNoise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

if __name__ == "__main__":
    if len(sys.argv) > 1:
        languages = sys.argv[1]
        custom_config = r'--oem 3 -l '+languages+' --psm 6'
    menu_options = (("Copy", None, systrayOption),)
    systray = SysTrayIcon('py.ico', 'Clipboard-OCR', menu_options)
    systray.start()
    
