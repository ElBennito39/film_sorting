import os
import constants

# return a list of full file names with given play_tag
def find_tags(play_tag):
    tag_results = []
    for path, currentDirectory, files in os.walk(constants.VID_PATH):
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
        if tag in constants.play_definition:
            print (tag)
            os.symlink("{}/Video Library/06-24-2022_Game#2_TidalWave".format(constants.VID_PATH)+"/"+file_name+".mp4","/Users/Sidekick/Desktop/{}".format(file_name)+".mp4")

            
# create aliases from list of files
def bulk_create_aliases(list):
    for file in list:
        create_aliases(file)

bulk_create_aliases(list)

