@echo off

set windowed=TRUE
set languages=eng
set anaconda_path="P:\Programme\Anaconda3"

call %anaconda_path%\Scripts\activate.bat 
if %windowed%==FALSE (
%anaconda_path%\pythonw.exe "clipboard_ocr.py" %languages%
)
if %windowed%==TRUE (
%anaconda_path%\pythonw.exe "clipboard_ocr_windowed.py" %languages%
)