# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 19:19:17 2021

@author: jahtzee
"""

# Import
import PySimpleGUI as sg
import tempfile
import pyperclip
import clipboard_ocr as co

# Definitions
custom_config = r'--oem 3 -l ger+rus+eng --psm 6'
temp = tempfile.gettempdir()

if __name__ == "__main__":
    layout = [[sg.Text('Output')], 
              [sg.InputText(key='-IN-')],
              [sg.Button("Read"), sg.Button("Copy"), sg.Button("Close")]]
    window = sg.Window('Clipboard OCR', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "Read":
            path = co.saveImageFromClipboard()
            result = co.OCRImageFromTemp(path)
            window['-IN-'].update(result)
        if event == "Copy":
            pyperclip.copy(values['-IN-'])
        if event == "Close":
            window.close()
    window.close()    

    
