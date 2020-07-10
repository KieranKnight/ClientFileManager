# clientFileManager
This application allows people to integrate large quantities of received files into an internal filing structure that might not match the structure the files have been received as.

All files that are added into the application have multiple options on how the file will be handled, where the file where be placed, etc.

The application offers a simple configuration setup where you are able to change settings by default meaning the next time the application is launched the new overrides will be used as default. 

A configuration option is avaliable for the output location. The output location is the top main folder where the received files will be integrated to. However, the files won't be placed directly into this folder. Each file will be placed into something like the following:
`{outputLocation}/{sequence}/{shot}/{option}/{file}`

On startup and if the output location get's changed, the location is quickly searched for the top and sub-folder. These folders will be stored and added to the Sequence and Shot drop down widgets to speed up the selection on where the file will be integrated to.

Users have the ability to track the files that get integrated by checking the Logging option.
They also have the ability to modify the logging location - This is where the actual logging file will be saved to on disk.

## Prerequisites
Make sure that you have Python 3.5+ and either PySide, PySide2, PyQt or PyQt2