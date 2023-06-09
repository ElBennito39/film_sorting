from PySide2.QtWidgets import QFileDialog, QDesktopWidget, QDialog
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtCore import QUrl, Qt
from datetime import timedelta
import os
import taggingFunctions

##FUNCTIONS BELOW

#Function to open video files in directories and their subdirectories and put them in a playlist
def open_directory(self):
    file_dialog = QFileDialog(self, "Open Directory")
    file_dialog.setFileMode(QFileDialog.DirectoryOnly)
    file_dialog.setOption(QFileDialog.DontUseNativeDialog)

    # Define your desired size here
    file_dialog.resize(1200, 800)

    # Centering file dialog
    qr = file_dialog.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    file_dialog.move(qr.topLeft())


    
    if file_dialog.exec_() == QFileDialog.Accepted:
        dir_name = file_dialog.selectedFiles()[0]

        if dir_name:
            self.playlist.undo_stack.clear()  # Clear the undo stack

            added_items = []  # Move added_items list here, outside the file loop

            # Find all video files in the directory and its subdirectories
            for root, dirs, files in os.walk(dir_name):
                for file_name in files:
                    
                    if file_name.endswith((".mp4", ".mov", ".mkv", ".avi", ".ts")):  # Add other video formats as needed
                        absolute_path = os.path.join(root, file_name)

                        # Create a playlist item with up to two directories and the file name
                        playlist_item = "/".join(absolute_path.split("/")[-3:])
                        
                        # Only add new item if it's not already in the playlist
                        if playlist_item not in self.file_paths:
                            self.file_paths[playlist_item] = absolute_path  # Add the absolute path to the playlist dictionary in the VideoWindow class
                            tags = taggingFunctions.load_tags_from_video(absolute_path) # Load the tagging Json from the file at the absolute path and add to the dictionary in the VideoWindow class
                            self.file_data[playlist_item] = tags # Load the tagging Json from the file at the absolute path and add to the dictionary in the VideoWindow class
                            added_items.append((self.playlist.count()-1,playlist_item,absolute_path, tags))
                        
            playlist_items = [item[1] for item in added_items]
            self.playlist.addItems(playlist_items)          
        
            # Add 'open_dir' action to the undo stack only once after all files have been processed
            self.playlist.undo_stack.append(('open_dir', added_items) if added_items else None)
            self.playlist.setFocus()



# Function to change the video file to play
def change_video(self, item):
    relative_path = item.text()

    if relative_path != '':
        # Look up the absolute path in the dictionary
        absolute_path = self.file_paths.get(relative_path)
        
        if absolute_path:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(absolute_path)))
            # Set the label's text to the absolute path
            self.file_path_label.setText(absolute_path)

# Function to filter the files
def filter_playlist(file_paths, file_data, filter_criteria): # takes in the playlist dictionaries for path and tagging data of each playlist item and the filter criteria dictionary
    pass

# Function to remove all items in playlist upon a filter activation, and palces them in the undo stack.
def remove_playlist_items(list_wiget, file_paths, file_data):
    playlist_items = [list_wiget.item(x) for x in range(list_wiget.count())]

    #remove items from playlist
    removed_items =[]
    for item in playlist_items:
        item_text = list_wiget.takeItem(item).text()
        file_path = file_paths.pop(item_text, None)
        file_tag_data = file_data.pop(item_text, None)
        removed_items.append((item, item_text, file_path, file_tag_data))
    
    return ('remove', removed_items) if removed_items else None

# Function to remove the currently selected items from the playlist
def remove_current_item(list_widget, file_paths, file_data):
    selected_items = list_widget.selectedItems()

    # Create a list of rows from the selected items
    rows = [list_widget.row(item) for item in selected_items]

    # Sort rows in reverse order
    rows.sort(reverse=True)

    removed_items = []
    # Remove items and corresponding file paths
    for row in rows:
        item_text = list_widget.takeItem(row).text()
        file_path = file_paths.pop(item_text, None)
        file_tag_data = file_data.pop(item_text, None)
        removed_items.append((row, item_text, file_path, file_tag_data))

    return ('remove', removed_items) if removed_items else None

# # Function to add items 
# def add_item(list_widget, file_paths, item_text, file_path):
#     # Add the item to the list widget and the file paths dictionary
#     list_widget.addItem(item_text)
#     file_paths[item_text] = file_path

#     return ('add', [(list_widget.count()-1, item_text, file_path)])

# Function to trigger the undo action from the action stack
def undo(list_widget, file_paths, file_data, undo_stack):
    if not undo_stack:
        return

    action, items = undo_stack.pop()
    if action == 'open_dir':
        for row, item_text, file_path, file_tag_data in items:
            list_widget.takeItem(row)
            file_paths.pop(item_text, None)
            file_data.pop(item_text, None)
            

    elif action == 'remove':
        for row, item_text, file_path, file_tag_data in reversed(items):
            # Only add item back if it doesn't already exist in the list
            if item_text not in file_paths:
                list_widget.insertItem(row, item_text)
                file_paths[item_text] = file_path
                file_data[item_text] = file_tag_data
    elif action == 'add':
        for row, item_text, file_path, file_tag_data in reversed(items):
            # Only remove item if it exists in the list
            if item_text in file_paths:
                list_widget.takeItem(row)
                file_paths.pop(item_text, None)
                file_data.pop(item_text, None)


# Function to toggle full screen
def toggle_window_size(self):
    if self.isMaximized():
        self.showNormal()  # Restore window size if it's maximized
    else:
        self.showMaximized()  # Maximize window if it's not already maximized

# Function to set the auto-play next setting
def set_auto_play_next(self, state):
    self.auto_play_next = state == Qt.Checked

def toggle_auto_play_next(self):
    self.auto_play_next_checkbox.setChecked(not self.auto_play_next_checkbox.isChecked())

# Function to reset the video playback position to '0' once the media finishes playing.
def check_media_status(self, status):
    if status == QMediaPlayer.EndOfMedia:
        self.media_player.setPosition(0)
        if self.auto_play_next_checkbox.isChecked():
            # Check if the current video is the last one in the playlist
            if self.playlist.currentRow() < self.playlist.count() - 1:
                # If not at the last item, go to the next video
                next_video(self)
                self.media_player.play()

# sets the speed of playback
def change_speed(self, value):
    self.media_player.setPlaybackRate(value / 10)
    self.speed_label.setText("{:.1f}x".format(value / 10))

# decreases the speed to slide value
def decrease_speed(self):
    self.speed_slider.setValue(self.speed_slider.value() -1)

# increases the speed to slider value
def increase_speed(self):
    self.speed_slider.setValue(self.speed_slider.value() +1)

# plays and pauses video based on the current state
def toggle_play_pause(self):
    if self.media_player.state() == QMediaPlayer.PlayingState:
        self.media_player.pause()
    else:
        self.media_player.play()
    
# method to update the play_pause action's text
def update_play_pause_action_text(self, state):
    if state == QMediaPlayer.PlayingState:
        self.play_pause_button.setText("Pause")
    else:
        self.play_pause_button.setText("Play")

# Fast forwards the video by 3 seconds
def fast_forward(self):
    position = self.media_player.position() + 3000  # Get the current position and add 3000 milliseconds to it
    self.media_player.setPosition(position)  # Set the new position

# Rewinds the video by 3 seconds
def rewind(self):
    position = self.media_player.position() - 3000  # Get the current position and subtract 3000 milliseconds from it
    self.media_player.setPosition(max(position, 0))  # Set the new position, don't go below 0

def next_video(video_window):
    current_row = video_window.playlist.currentRow()
    total_items = video_window.playlist.count()

    # Check if we are already at the last item
    if current_row >= total_items - 1:
        # If we are at the last item, stop the player
        video_window.media_player.stop()
        return

    # If we are not at the last item, go to the next item
    video_window.playlist.setCurrentRow(current_row + 1)
    change_video(video_window, video_window.playlist.currentItem())


# Change to previous item in the playlist - call change_video to change the video.
def prev_video(self):
    current_row = self.playlist.currentRow()
    if current_row > 0:
        self.playlist.setCurrentRow(current_row - 1)
        self.change_video(self.playlist.currentItem())    

# Set the position of the video to the slider position
def set_position(self, position):
    self.media_player.setPosition(position)

# Update the slider position as the video plays
def position_changed(self, position):
    self.position_slider.setValue(position)
    self.position_label.setText(f"Time:    {format_time(position)}    /") #update the position label on position change

# Update the range of the slider when the video duration changes (like when a new video is selected)
def duration_changed(self, duration):
    self.position_slider.setRange(0, duration)
    self.duration_label.setText(format_time(duration)) #update the duration label on duration change

def format_time(millis):
    formatted_time = str(timedelta(milliseconds=millis))
    seconds_index = formatted_time.find('.')
    if seconds_index != -1:  # If there are decimal places
        formatted_time = formatted_time[:seconds_index+2]  # Only keep one decimal place
    return formatted_time

# function to change widget visibility
def toggle_widget_visibility(widget):
    # This function toggles the visibility of the given widget
    widget.setVisible(not widget.isVisible())

def toggle_checkbox(checkbox):
    current_state = checkbox.isChecked()
    checkbox.setChecked(not current_state)
