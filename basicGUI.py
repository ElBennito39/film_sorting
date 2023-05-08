import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import functools

def open_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        video_player.load(file_path)
        video_player.play()

def toggle_tag(tag_button):
    if tag_button.config('relief')[-1] == 'sunken':
        tag_button.config(relief="raised", bg='SystemButtonFace')
    else:
        tag_button.config(relief="sunken", bg='green')

root = tk.Tk()
root.title("Video Tagger")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Subtract a few pixels to avoid overlapping with the taskbar or other screen elements
root.geometry(f"{screen_width - 10}x{screen_height - 10}")


frame = tk.Frame(root, bg="black")
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

video_player = TkinterVideo(master=frame)
video_player.pack(fill=tk.BOTH, expand=True)

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
tagging_frame.pack(pady=10)

# Section 0: Goal fore/against and penalty taken/drawn
section0 = tk.Frame(tagging_frame)
section0.grid(row=0, column=0)

tag_buttons_goals_penalties = ["Goal For", "Goal Against", "Penalty Drawn", "Penalty Taken"]
for i, tag in enumerate(tag_buttons_goals_penalties):
    tag_button = tk.Button(section0, text=tag, width=10, relief="raised")
    tag_button.config(command=functools.partial(toggle_tag, tag_button))
    tag_button.grid(row=i % 2, column=i // 2, padx=5, pady=5)

# Section 1: Text entry and Add/Remove buttons
section1 = tk.Frame(tagging_frame)
section1.grid(row=0, column=2, columnspan=1)

tag_entry = tk.Entry(section1, width=10)
tag_entry.pack(side=tk.LEFT, padx=5)

add_tag_button = tk.Button(section1, text="Add Tag", width=10)
add_tag_button.pack(side=tk.LEFT, padx=5)

remove_tag_button = tk.Button(section1, text="Remove Tag", width=10)
remove_tag_button.pack(side=tk.LEFT, padx=5)

# Section 2: Tag buttons 7-12 in a 2x3 grid
section2 = tk.Frame(tagging_frame)
section2.grid(row=1, column=0)

tag_buttons_7_12 = ["Tag7", "Tag8", "Tag9", "Tag10", "Tag11", "Tag12"]
for i, tag in enumerate(tag_buttons_7_12):
    tag_button = tk.Button(section2, text=tag, width=10, relief="raised")
    tag_button.config(command=functools.partial(toggle_tag, tag_button))
    tag_button.grid(row=i % 2, column=i // 2, padx=5, pady=5)

# Section 3: Space out attribute from play-type taggings
section3 = tk.Frame(tagging_frame)
section3.grid(row=1, column=1)

# Section 4: Numpad-like grid with an extra button for 0
section4 = tk.Frame(tagging_frame)
section4.grid(row=1, column=2)

numpad_tags = ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5", "Tag6", "Tag7", "Tag8"]
for i, tag in enumerate(numpad_tags):
    tag_button = tk.Button(section4, text=tag, width=10, relief="raised")
    tag_button.config(command=functools.partial(toggle_tag, tag_button))
    tag_button.grid(row=i % 3, column=i // 3, padx=5, pady=5)


# Menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_video)

root.mainloop()
