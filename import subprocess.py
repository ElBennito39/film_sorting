import subprocess

# bashCommand = "alisma -a \"/Users/Sidekick/Desktop/PHC 15U/Video Library/06-24-2022_Game#2_TidalWave/02_01_NZO_WWing_Support.mp4\" \"/Users/Sidekick/Desktop/PHC 15U/Post Scout\" "
# bashCommand = "osascript -e 'tell application \"Finder\"' -e 'make new alias to file (posix file \"/Users/Sidekick/Desktop/PHC 15U/Video Library/06-24-2022_Game#2_TidalWave/02_01_NZO_WWing_Support.mp4\") at desktop' -e 'end tell'"


#osascript -e 'tell application "Finder"' -e 'make new alias to file (posix file "/Users/me/Library/Preferences/org.herf.Flux.plist") at desktop' -e 'end tell'
#bashCommand = 'osascript -e "tell application \"Finder\""' -e "make new alias to file (posix file \"/Users/Sidekick/Desktop/PHC\ 15U/Video\ Library/06-24-2022_Game#2_TidalWave/02_01_NZO_WWing_Support.mp4\") at desktop" -e "end tell"
 
step_1 = "osascript -e "
step_2 = "'tell application "
step_3 = '\"Finder\"' + "' "
step_4 = "-e 'make new alias to file (posix file "
step_5 = '\"/Users/Sidekick/Desktop/PHC\ 15U/Video\ Library/06-24-2022_Game#2_TidalWave/02_01_NZO_WWing_Support.mp4\") '
step_6 = "at desktop' -e 'end tell'"

bashCommand = step_1+step_2+step_3+step_4+step_5+step_6

print(bashCommand)

process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()