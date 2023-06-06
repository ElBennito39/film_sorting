from PySide2.QtWidgets import QFileDialog, QButtonGroup
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtCore import QUrl, Qt
from datetime import timedelta
import os

##FUNCTIONS BELOW

#function to open video files in directories and their subdirectories and put them in a playlist
def open_directory(self):
    dir_name = QFileDialog.getExistingDirectory(self, "Open Directory")
    if dir_name:
        # Find all video files in the directory and its subdirectories
        for root, dirs, files in os.walk(dir_name):
            for file_name in files:
                if file_name.endswith((".mp4", ".mov", ".mkv", ".avi", ".ts")):  # Add other video formats as needed
                    absolute_path = os.path.join(root, file_name)

                    # Create a playlist item with up to two directories and the file name
                    playlist_item = "/".join(absolute_path.split("/")[-3:])
                    
                    # Only add new item if it's not already in the playlist
                    if playlist_item not in self.file_paths:
                        self.file_paths[playlist_item] = absolute_path  # Add the absolute path to the dictionary
                        self.playlist.addItem(playlist_item)
        # # After opening the directory and populating the playlist
        # self.playlist.setFocus()  # Set focus to the playlist widget
        # self.playlist.setCurrentRow(0)  # Optionally, select the first item in the playlist

                        # # Read the metadata of the file and load the tags
                        # media_content = QMediaContent(QUrl.fromLocalFile(absolute_path))
                        # tag_string = media_content.metaData("comments")

                        # if tag_string:
                        #     try:
                        #         tag_dict = json.loads(tag_string)
                        #         # TODO: Update the UI to display the loaded tags
                        #     except json.JSONDecodeError:
                        #         print(f"Failed to parse tags for file: {absolute_path}")


# Function to change the video file to play
def change_video(self, item):
    relative_path = item.text()

    # # prompt with a message box if there are unsaved changes on change video
    # if self.unsaved_changes:
    #     msg = QMessageBox()
    #     msg.setIcon(QMessageBox.Warning)
    #     msg.setText("There are unsaved changes.")
    #     msg.setInformativeText("Do you want to save your changes?")
    #     msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    #     msg.setDefaultButton(QMessageBox.Save)
    #     retval = msg.exec_()

    #     if retval == QMessageBox.Save:
    #         # Save changes function here
    #         pass
    #     elif retval == QMessageBox.Discard:
    #         # Continue without saving changes
    #         pass
    #     elif retval == QMessageBox.Cancel:
    #         # Do not proceed with the video change
    #         return

    if relative_path != '':
        # Look up the absolute path in the dictionary
        absolute_path = self.file_paths.get(relative_path)
        
        if absolute_path:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(absolute_path)))
            # Set the label's text to the absolute path
            self.file_path_label.setText(absolute_path)

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

# # Function to reset the video playback position to '0' once the media finishes playing.
# def check_media_status(self, status):
#     if status == QMediaPlayer.EndOfMedia:
#         self.media_player.setPosition(0)
#         if self.auto_play_next_checkbox.isChecked():
#             next_video(self)
#             self.media_player.play()
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

# # Change to next item in the playlist - call change_video to change the video.
# def next_video(video_window):
#     current_row = video_window.playlist.currentRow()
#     if current_row < video_window.playlist.count() - 1:
#         video_window.playlist.setCurrentRow(current_row + 1)
#         change_video(video_window, video_window.playlist.currentItem())
#     else:
#         video_window.media_player.stop()
# Change to next item in the playlist - call change_video to change the video.
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

def activate_button(button_group):
    buttons = [button for button in button_group.buttons() if button.isChecked()]
    for button in buttons:
        button.toggle()

# function to change widget visibility
def toggle_widget_visibility(widget):
    # This function toggles the visibility of the given widget
    widget.setVisible(not widget.isVisible())

def toggle_checkbox(checkbox):
    current_state = checkbox.isChecked()
    checkbox.setChecked(not current_state)



# def save_tags(self):
#     # Extract the tag values from your input widgets
#     # # For example, if you had a QLineEdit for the user to input a title:
#     # title = self.title_input.text()

#     # Same for other types of tags...
#     # Create a dictionary with your tag values
#     tag_dict = {"title": title, {}}

#     # Convert the dictionary to a JSON string
#     json_string = json.dumps(tag_dict)

#     # Write the JSON string to the file's comments metadata
#     self.current_video.metadata["comments"] = json_string

#     # Reset the unsaved changes flag
#     self.unsaved_changes = False
