import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import functools, os



# Function to open a single video file
def open_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        video_player.load(file_path)
        video_player.play()
        load_playlist([file_path])  # load the playlist with the single video

# Function to open a directory and load all video files into the playlist
def open_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        # get all video files in the directory
        video_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(('.mp4', '.avi'))]  # add more formats if needed
        load_playlist(video_files)  # load the playlist with the video files

# Function to load a list of video files into the playlist
def load_playlist(video_files):
    playlist.clear()  # clear the existing playlist
    playlist_listbox.delete(0, tk.END)  # clear the Listbox widget

    max_width = 25  # set a maximum width
    longest_name = max([os.path.basename(f) for f in video_files], key=len, default='')
    if len(longest_name) > max_width:
        playlist_listbox.config(width=max_width)
    else:
        playlist_listbox.config(width=len(longest_name))

    for file_path in video_files:
        playlist.append(file_path)  # add the file to the playlist
        file_name = os.path.basename(file_path)
        playlist_listbox.insert(tk.END, file_name)  # add the file to the Listbox widget


# Function to play a video file at the given index in the playlist
def play_video(index):
    video_player.load(playlist[index])
    video_player.play()

# Event handler for selection changes in the Listbox widget
def on_playlist_selection_change(event):
    selected_indices = playlist_listbox.curselection()  # get the selected indices
    if selected_indices:
        play_video(selected_indices[0])  # play the selected video


# Function for tag buttons to toggle when selected
def toggle_tag(button):
    if button.config("relief")[-1] == "raised":
        button.config(relief="sunken", background="NavyBlue", foreground="white")
    else:
        button.config(relief="raised", background=default_button_color, foreground="black")

# Function for the play strength tag buttons, so that only one can be selected at a time
def toggle_strength_tag(button):
    global last_pressed_strength_button
    # If a button was previously pressed, reset it to its original state
    if last_pressed_strength_button is not None:
        last_pressed_strength_button.config(relief="raised", background=default_button_color, foreground="black")
    # If the same button was pressed again, do not change its state
    if last_pressed_strength_button != button:
        button.config(relief="sunken", background="NavyBlue", foreground="white")
        last_pressed_strength_button = button
    else:
        last_pressed_strength_button = None
        
# Function to connect hot key bindings to the toggle of the button 
def on_key_press(event, tag_button):
    toggle_tag(tag_button)



# Create the TKinter GUI

root = tk.Tk()
root.title("Video Tagger")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Subtract a few pixels to avoid overlapping with the taskbar or other screen elements
root.geometry(f"{screen_width - 10}x{screen_height - 10}")

# Create frame for the video player
frame = tk.Frame(root, bg="black")
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

video_player = TkinterVideo(master=frame)
video_player.pack(fill=tk.BOTH, expand=True)

# Create a Listbox widget to display the playlist
playlist_listbox = tk.Listbox(root)
playlist_listbox.pack(side=tk.LEFT, fill=tk.Y)
playlist_listbox.bind('<<ListboxSelect>>', on_playlist_selection_change)

# Initialize the playlist
playlist = []

# Create a frame to hold the toolbar
toolbar = tk.Frame(root, bd=1, relief=tk.SUNKEN)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Playback buttons
play_button = tk.Button(toolbar, text="Play", width=10, command=video_player.play)
play_button.grid(row=0, column=0, padx=5)

pause_button = tk.Button(toolbar, text="Pause", width=10, command=video_player.pause)
pause_button.grid(row=0, column=1, padx=5)

stop_button = tk.Button(toolbar, text="Stop", width=10, command=video_player.stop)
stop_button.grid(row=0, column=2, padx=5)

# Navigation buttons
prev_button = tk.Button(toolbar, text="Previous", width=10)
prev_button.grid(row=0, column=3, padx=5)

next_button = tk.Button(toolbar, text="Next", width=10)
next_button.grid(row=0, column=4, padx=5)

# Tagging mechanism
tagging_frame = tk.Frame(root)
tagging_frame.pack(pady=10, fill=tk.X)
# create a dummy button to get the background color to use in toggle_tag() so it can reset the background color on click
dummy_button = tk.Button(root)
default_button_color = dummy_button.cget("background")

# Configure columns to expand proportionally
tagging_frame.columnconfigure(0, weight=1)
tagging_frame.columnconfigure(1, weight=1)
tagging_frame.columnconfigure(2, weight=1)

# Section 0: Goal fore/against and penalty taken/drawn
section0 = tk.Frame(tagging_frame)
section0.grid(row=0, column=0)

tag_buttons_goals_penalties = ["Goal For", "Goal Against", "Penalty Drawn", "Penalty Taken"]
for i, tag in enumerate(tag_buttons_goals_penalties):
    tag_button = tk.Button(section0, text=tag, width=15, relief="raised")
    tag_button.config(command=functools.partial(toggle_tag, tag_button))
    tag_button.grid(row=i % 2, column=i // 2, padx=5, pady=5)

# # Section 3: Space out attribute from play-type taggings by creating a Label to span column 1 to a set width
# section3 = tk.Label(tagging_frame, width=30)
# section3.grid(row=0, column=1)

# Section 1.5: Text display
section1_5 = tk.Frame(tagging_frame)
section1_5.grid(row=0, column=1)

text_display = tk.Label(section1_5, text="True Man Power", bg="white", relief="sunken", width=20)
text_display.pack(padx=5, pady=5)

# # Section 1: Text entry and Add/Remove buttons
# section1 = tk.Frame(tagging_frame)
# section1.grid(row=0, column=2, columnspan=1)

# tag_entry = tk.Entry(section1, width=20)
# tag_entry.pack(side=tk.LEFT, padx=5)

# add_tag_button = tk.Button(section1, text="Add Tag", width=10)
# add_tag_button.pack(side=tk.LEFT, padx=5)

# remove_tag_button = tk.Button(section1, text="Remove Tag", width=10)
# remove_tag_button.pack(side=tk.LEFT, padx=5)

# Section 2: Tag buttons for play strength
section2 = tk.Frame(tagging_frame)
section2.grid(row=1, column=0)

# maintain a reference to the last pressed button in the Play Strength section
last_pressed_strength_button = None

tag_buttons_play_strength = ["5 v 4", "4 v 5", "5 v 3", "3 v 5", "4 v 3", "3 v 4"]
for i, tag in enumerate(tag_buttons_play_strength):
    tag_button = tk.Button(section2, text=tag, width=10, relief="raised")
    tag_button.config(command=functools.partial(toggle_strength_tag, tag_button))
    tag_button.grid(row=i % 2, column=i // 2, padx=5, pady=5)

# Section 5: Tag buttons Extra Attacker and Net Empty
section5 = tk.Frame(tagging_frame)
section5.grid(row=1, column=1)

tag_buttons_empty_net = ["Extra Attacker", "Opp. Net Empty"]
for i, tag in enumerate(tag_buttons_empty_net):
    tag_button = tk.Button(section5, text=tag, width=15, relief="raised")
    tag_button.config(command=functools.partial(toggle_tag, tag_button))
    tag_button.grid(row=i % 2, column=i // 2, padx=5, pady=5)



# Section 4: Custom grid layout for Play-type
section4 = tk.Frame(tagging_frame)
section4.grid(row=0, column=2, rowspan=2)

#button creation
numpad_tags = ["DZCoverage", "Backchecking", "NZForehecking", "OZForecheck", "BreakOut", "Regrouping", "NZAttack",  "OZAttack"]
grid_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
for tag, position in zip(numpad_tags, grid_positions):
    tag_button = tk.Button(section4, text=tag, width=10, relief="raised")
    tag_button.config(command=functools.partial(toggle_tag, tag_button))
    tag_button.grid(row=position[0], column=position[1], padx=5, pady=5)
    
#binding numbers to play type buttons with a function 
def bind_hotkeys():
    for i in range(8):
        number_hotkey = str(i+1)
        numpad_hotkey = 'KP_' + str(i+1)
        button = section4.grid_slaves(row=i//4, column=i%4)[0]
        root.bind(number_hotkey, functools.partial(on_key_press, tag_button=button))
        root.bind('<' + numpad_hotkey + '>', functools.partial(on_key_press, tag_button=button)) # key symbols for the numpad keys should be wrapped with < and > 
#call that function
bind_hotkeys()



# Menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_video) # command to open a file
file_menu.add_command(label="Open Directory", command=open_directory)  # command to open a directory

root.mainloop()
