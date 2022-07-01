# Game Footage Organizer by Play Type Attribute
#
# Store Game Film in one 'library'
# Create Symlink of each clip in ALL of the cooresponding play attribute folder
# 
# 
# functions needed
# 
# create alias of clip in destination:
# 
# iterate a search file names for play attribute
#  
# 
# 
# finding files with one play attribute tag

import os
import constants

#delete legacy symlinks
def del_legacy_syms():
    for path, currentDirectory, files_in_directory in os.walk(constants.DEST_PATH):
        for filename in files_in_directory:
            os.remove(path+"/"+filename)
        
del_legacy_syms()

# # takes in a string and returns a list of tuples with full file path and file name for each file in directory
#Map Files to list or tuples
def find_tags():
    tag_results = []
    for path, currentDirectory, files_in_directory in os.walk(constants.VID_PATH):
        print ("path")
        print (path)
        print ("filenames in directory")
        print (files_in_directory)
        for filename in files_in_directory:
            tag_results.append([path,filename])
    return tag_results


tag_tuples= find_tags()
print ("tag_tuples")
print (tag_tuples)

#unpack tuple list into list of file names and list of file paths
# path_list, file_list = zip(*tag_tuples)


# take in file_list, for each file in that list create symlink to each path in that tags directory

def create_symlink(list):

    for tuple in list: 

        file_full_name = tuple[1]
        file_name = file_full_name.replace('.mp4','')
        
        tag_list = file_name.split('_')
            
        for tag in tag_list:
            if tag in constants.play_definition:
                print ("tag")
                print (tag)
                print ("file_full_name")
                print (file_full_name)
                print ("play_definition[tag]")
                print (constants.play_definition[tag])
            

                os.symlink(tuple[0]+"/"+file_full_name,f"{constants.play_definition[tag]}{file_full_name}")



create_symlink(tag_tuples)            

