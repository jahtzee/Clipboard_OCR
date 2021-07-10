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
custom_config = r'--oem 3 --psm 6'
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
    #Task Tray
    menu_options = (("Copy", None, systrayOption),)
    systray = SysTrayIcon('py.ico', 'Clipboard-OCR', menu_options)
    systray.start()
    
    #Proper GUI
    """
        layout = [[sg.Text('Output')], 
              [sg.InputText(key='-IN-')],
              [sg.Button("Read"), sg.Button("Copy"), sg.Button("Close")]]
    window = sg.Window('Clipboard OCR', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "Read":
            path = saveImageFromClipboard()
            result = OCRImageFromTemp(path)
            window['-IN-'].update(result)
        if event == "Copy":
            pyperclip.copy(values['-IN-'])
        if event == "Close":
            window.close()
    window.close()    
    """
    
