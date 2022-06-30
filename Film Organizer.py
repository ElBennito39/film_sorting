import os

for path, currentDirectory, files in os.walk(VID_PATH):
    print (path)
    print (files)