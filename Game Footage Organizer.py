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
from mac_alias import Alias

# build dictionary of play types and alias destination folders
play_definition = {
    "DZC":"/Users/Sidekick/Desktop/PHC 15U/Post Scout/DZCoverage",
    "BO":"/Users/Sidekick/Desktop/PHC 15U/Post Scout/Breakout (BO)",
    "NZF":"/Users/Sidekick/Desktop/PHC 15U/Post Scout/NZForecheck",
}
    

# return a list of full file paths with given play_tag
def find_tag(play_tag):
    tag_results = []
    for path, currentDirectory, files in os.walk("/Users/Sidekick/Desktop/PHC 15U"):
       for file in files:
        if play_tag in file:
            # tag_results.append(path+'/'+file)
            tag_results.append(file)
    return tag_results
    print (tag_results)

list = find_tag ("DZC")

# take in tag results, create alias to each path in that tags directory

def create_aliases(file_name):
    # file_path = '02_13_BO_DZC_NZF.mp4'
    file_name = file_name.replace('.mp4','')
    
    tag_list = file_name.split('_')
        
    for tag in tag_list:
        Alias.for_file(play_definition[tag])

#
# create aliases from list of files

def bulk_create_aliases(list):
    for file in list:
        create_aliases(file)

bulk_create_aliases(list)




# 

# 