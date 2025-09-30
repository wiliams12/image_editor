# Image Editor with web interface
- this project is educational. 
- Image filters and basic GUI learning project.
- not all approaches are optimal (handling images as three-dimensional arrays, ignoring the use of libraries...)
- simple filters and cropping, no image deformations implemented

# Features
- simple filters ✅
- color chanels editor ✅
- cropping ✅
- brightness, exposition... ✅
- painting ✅

# Technologies
- PyQt for GUI
- uses numpy to work with images. Though not very effective in some cases, done for educational purposes.
- uses OpenCV for faster kernel operation

# How to use
- either run it as a Python or you can make it into an executable
1. install PyInstaller 
```pip3 install PyInstaller```
2. create the executable
```pyinstaller --noconsole --onedir --icon=static\icon.png src/main.py```
3. the executable will be located in dist/main/
