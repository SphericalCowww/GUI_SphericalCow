# Spherical Cow Desktop Pet

### Using pyinstaller-3.7 to create an executable:
Create and activate a virtual environment (in packageEnv/):
  
    virtualenv sphericalCowEnv
    source sphericalCowEnv/bin/activate
Installed only PyQt5:

    pip3 install PyQt5
Use the pyinstaller to package the file (note: to convert png to icns, specific image dimension is required):

    pyinstaller-3.7 --onefile --windowed --icon=cowAIcon.icns --name SphericalCow desktopPetExe.py
Modify SphericalCow.spec following the SphericalCowExample.spec, then do,

    pyinstaller-3.7 SphericalCow.spec
Note that the exePath() function in the desktopPetExe.py is essential for the executable to find the right path. For debuging run:

    ./SphericalCow in terminal to debug.
Deactivate the virtual environment

    deactivate
    
    
