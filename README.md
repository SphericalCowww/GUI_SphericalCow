# Spherical Cow Desktop Pet

https://user-images.githubusercontent.com/55116073/141663986-5da4c3d9-5049-4b37-927a-5fabdf7f98fd.mov

### Starting the program:
Double click SphericalCowMac in a mac computer or double click SphericalCowWindows in a windows computer to start the program. To run it with python, go to package/ and do:

    python3 desktopPet.py

### Other programs:
- QMovieExp.py: runs test.gif with PyQt5
- pngTrans.py: make the background white region of a .png file transparent
- pngToGif.py: combines a list of .png files to a .gif file

### Using pyinstaller-3.7 to package the program:
Create and activate a virtual environment (was done in packageEnv/):
  
    virtualenv sphericalCowEnv
    source sphericalCowEnv/bin/activate
Installed only PyQt5:

    pip3 install PyQt5
Use the pyinstaller to package the file (note: to convert a .png file to a .ico/.icns, specific image dimension is required. They were done using online tools):

    pyinstaller-3.7 --onefile --windowed --icon=cowAIcon.ico --name SphericalCow desktopPetMacApp.py (in mac)
    pyinstaller-3.7 --onefile --windowed --icon=cowAIcon.icns --name SphericalCow desktopPetWinExe.py (in windows)
Modify SphericalCow.spec following the SphericalCowExample.spec, then do,

    pyinstaller-3.7 SphericalCow.spec
Note that the exePath() function in the desktopPetExe.py is essential for the executable to find the right path. For debuging run:

    ./SphericalCow in terminal to debug.
Deactivate the virtual environment

    deactivate
    
    
