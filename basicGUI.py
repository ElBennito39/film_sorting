import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo

def open_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        video_player.load(file_path)
        video_player.play()

root = tk.Tk()
root.title("Video Tagger")
root.geometry("800x600")

frame = tk.Frame(root, bg="black")
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

video_player = TkinterVideo(frame, scaled=True)
video_player.pack(fill=tk.BOTH, expand=True)

play_button = tk.Button(root, text="Play", width=10, command=video_player.play)
play_button.pack(side=tk.LEFT, padx=5)

pause_button = tk.Button(root, text="Pause", width=10, command=video_player.pause)
pause_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(root, text="Stop", width=10, command=video_player.stop)
stop_button.pack(side=tk.LEFT, padx=5)

prev_button = tk.Button(root, text="Previous", width=10)
prev_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(root, text="Next", width=10)
next_button.pack(side=tk.LEFT, padx=5)

tag_entry = tk.Entry(root, width=30)
tag_entry.pack(side=tk.RIGHT, padx=5)

add_tag_button = tk.Button(root, text="Add Tag", width=10)
add_tag_button.pack(side=tk.RIGHT, padx=5)

remove_tag_button = tk.Button(root, text="Remove Tag", width=10)
remove_tag_button.pack(side=tk.RIGHT, padx=5)

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_video)

root.mainloop()
