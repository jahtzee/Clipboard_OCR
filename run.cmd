@echo on

set anaconda_path="P:\Programme\Anaconda3"

call %anaconda_path%\Scripts\activate.bat 
%anaconda_path%\pythonw.exe "clipboard_ocr.py"