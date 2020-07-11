# clientFileManager
This application supports the integration of large quantities of files into an internal filing structure.

All files that are added into the application have multiple options on how the file will be handled, where the file where be placed, etc.

A configuration option is avaliable for the output location. The output location is the top main folder where the received files will be integrated to. However, the files won't be placed directly into this folder. Each file will be placed into something like the following:
`{outputLocation}/{sequence}/{shot}/{option}/{file}`

## How To Use
1) Add the package to your environment path.
2) Within a terminal navigate to the package.
3) Run ~ `python .\clientFileManager\launch_manager.py`

## Default Usage
If no configure settings are changed the application will run as follows;

* All output locations will be placed into your documents area - `C:\Users\{user}\Documents\clientFileManager\integrate`
* * If this folder has been used before, it will take the top two folders and add these as options to the Sequence and Shot widget per file (The same functionality works if the output location has been changed too)

* All logging outputs will be placed intoyour documents area - `C:\Users{user}\Documents\clientFileManager\integrate`

## Prerequisites
Make sure that you have Python 3.5+ and either PySide, PySide2, PyQt or PyQt2
