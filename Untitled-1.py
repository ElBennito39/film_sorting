
# osascript -e 'tell application \"Finder\"' -e 'make new alias to file (posix file \"/Users/Sidekick/Desktop/PHC\ 15U/Video\ Library/06-24-2022_Game#2_TidalWave/02_01_NZO_WWing_Support.mp4\") at desktop' -e 'end tell'

# osascript -e 'tell application "Finder"' -e 'make new alias to file (posix file "/Users/me/Library/Preferences/org.herf.Flux.plist") at desktop' -e 'end tell'

# osascript -e 'tell application "Finder"' -e 'make new alias to file (posix file /Users/Sidekick/Desktop/Movie_6-29-22_DZC_BO.mov) at desktop' -e 'end tell'
# 

from ctypes.wintypes import tagMSG
import os

def find_tags(play_tag):
    tag_results = []
    for path, currentDirectory, files in os.walk("/Users/Sidekick/Desktop/PHT 15U/Video Library"):
       for file in files:
        if play_tag in file:
             tag_results.append([path,file])
    print (tag_results)
    return tag_results

find_tags("DZC")