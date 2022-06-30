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
from ctypes.wintypes import tagMSG
import os

#path placeholder for video link destinations

DEST_PATH = "/Users/Sidekick/Desktop/PHC 15U/Post Scout"
VID_PATH= "/Users/Sidekick/Desktop/PHT 15U/Video Library"

# build dictionary of play types and symlink destination folders
play_definition = {
    "DZC":"{}/DZCoverage".format(DEST_PATH),
    "BO":"{}/Breakout (BO)".format(DEST_PATH),
    "NZF":"{}/NZForecheck".format(DEST_PATH),
}
    

# return a list of full file names with given play_tag
def find_tags(play_tag):
    tag_results = []
    for path, currentDirectory, files in os.walk(VID_PATH):
       for file in files:
        if play_tag in file:
             tag_results.append(file)
    return tag_results
    print (tag_results)
# list of all found tags as defined by tag_results

list = find_tags ("DZC")

# take in tag results, create alias to each path in that tags directory

def create_symlink(file_name):

    file_name = file_name.replace('.mp4','')
    
    tag_list = file_name.split('_')
        
    for tag in tag_list:
        if tag in play_definition:
            print (tag)
            os.symlink("{}/Video Library/06-24-2022_Game#2_TidalWave".format(VID_PATH)+"/"+file_name+".mp4","/Users/Sidekick/Desktop/{}".format(file_name)+".mp4")

            

#
# create aliases from list of files

def bulk_create_aliases(list):
    for file in list:
        create_aliases(file)

bulk_create_aliases(list)

