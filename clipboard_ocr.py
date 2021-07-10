# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 19:19:17 2021

@author: jahtzee
"""

# Import
import os
#import PySimpleGUI as sg
import cv2
import pytesseract
from PIL import ImageGrab
import tempfile
import pyperclip
from infi.systray import SysTrayIcon

# Definitions
custom_config = r'--oem 3 -l ger+rus+eng --psm 6'
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
    string = str(pytesseract.image_to_string(img))
    os.remove(temp+'\ocr_tmp.PNG')
    string = string.replace("\f","")
    string.strip()
    return string

def systrayOption(systray):
    path = saveImageFromClipboard()
    pyperclip.copy(OCRImageFromTemp(path))  

if __name__ == "__main__":
    menu_options = (("Copy", None, systrayOption),)
    systray = SysTrayIcon('py.ico', 'Clipboard-OCR', menu_options)
    systray.start()
    
