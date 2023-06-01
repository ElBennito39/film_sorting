#Importing
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtCore import QUrl, QSize, Qt
from PySide2.QtGui import QKeySequence
from datetime import timedelta
import os


# Create a main window class
class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide2 Video Player") #title the media palyer

        # Store the current directory
        self.current_dir = None

        # Add a list of directories for playlists
        self.dirs_list = []
        self.file_paths = {}  # List to store absolute paths

        # Set initial size of the window to 60% of the screen size
        screen_geometry = QApplication.primaryScreen().geometry()
        self.resize(screen_geometry.width() * 0.6, screen_geometry.height() * 0.6)

        # Set up the media player and video widget
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()

        # set the size policy
        self.video_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Create QActions for playback functionality
        self.stop_action = QAction("Stop", self)
        self.fast_forward_action = QAction("Fast Forward", self)
        self.rewind_action = QAction("Rewind", self)
        self.next_action = QAction('Next', self)
        self.prev_action = QAction('Previous', self)

        # Connect the playback actions to the respective methods
        self.stop_action.triggered.connect(self.media_player.stop)
        self.fast_forward_action.triggered.connect(self.fast_forward)
        self.rewind_action.triggered.connect(self.rewind)
        self.next_action.triggered.connect(self.next_video)
        self.prev_action.triggered.connect(self.prev_video)
        
        # Create QToolButton so we can control the size of play-pause function interfacte
        self.play_pause_button = QToolButton()
        self.play_pause_button.setText("Play")
        
        # Connect the play pause button to the respective method
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.play_pause_button.setFixedWidth(self.play_pause_button.fontMetrics().width('Pause') + 20)

        # Create a checkbox for auto-play next
        self.auto_play_next_checkbox = QCheckBox("Auto-Next")
        self.auto_play_next_checkbox.stateChanged.connect(self.set_auto_play_next)


        # Store the auto-play next setting
        self.auto_play_next = False

        # Create a toolbar and add the buttons, actions, checkbox
        self.toolbar = self.addToolBar("Playback")
        self.toolbar.addWidget(self.play_pause_button)
        self.toolbar.addSeparator() 
        self.toolbar.addAction(self.stop_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.rewind_action)
        self.toolbar.addAction(self.fast_forward_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.prev_action)
        self.toolbar.addAction(self.next_action)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.auto_play_next_checkbox)



        # Add video position slider
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.position_slider.setFixedHeight(15)

        # Add labels for video position and duration
        self.position_label = QLabel()
        self.duration_label = QLabel()

        # Connect the media player's positionChanged and durationChanged signals
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        # Add speed slider selection
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(2)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(10)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksAbove)
        self.speed_slider.valueChanged.connect(self.change_speed)

        # Add a label for playback speed
        self.speed_label = QLabel()

        # Create playlist widget
        self.playlist = QListWidget()

        ### Window Layout ###

        # Create a central widget to anchor boxes of widgets
        central_widget = QWidget() #create central widget
        self.setCentralWidget(central_widget)#set is as central

        # Create main layout
        main_layout = QVBoxLayout()

        #Create a label to display the file path
        self.file_path_label = QLabel()  # File path label
        
        #Add the label to the main layout
        main_layout.addWidget(self.file_path_label)

        # Create a horizontal splitter for the top half of the window
        top_half = QSplitter(Qt.Horizontal)
        top_half.addWidget(self.playlist)
        top_half.addWidget(self.video_widget)
        top_half.setSizes([self.width() / 5, 4 * self.width() / 5])

        # Add the top_half splitter to the main layout
        main_layout.addWidget(top_half, stretch=1)

        # Create a layout for the position slider and label
        position_section = QHBoxLayout()
        position_section.addWidget(self.position_slider)
        position_section.addWidget(self.position_label)
        position_section.addWidget(self.duration_label)

        position_widget = QWidget()
        position_widget.setLayout(position_section)

        # Add the position_section layout to the main layout
        main_layout.addWidget(position_widget)

        # Add tool bar to main layout
        main_layout.addWidget(self.toolbar)

        # Create a layout for the speed slider and label
        speed_section = QHBoxLayout()
        speed_section.addWidget(self.speed_slider)
        speed_section.addWidget(self.speed_label)
        speed_widget = QWidget()
        speed_widget.setLayout(speed_section)

        # Add the speed_section layout to the main layout
        main_layout.addWidget(speed_widget)

        # Assign the main layout to the central widget
        central_widget.setLayout(main_layout)

        # Set a minimum size for the video widget
        self.video_widget.setMinimumSize(500, 400)

        # Set maximum heights for the button and slider sections
        speed_widget.setMaximumHeight(75)
        position_widget.setMaximumHeight(75)

        ### Connect media and signals ###

        # Set the video output from media player to widget
        self.media_player.setVideoOutput(self.video_widget)

        # Connect the media player's state changed signal to handle resizing the window
        self.media_player.stateChanged.connect(self.resize_to_video)

        # Connect the media player's state signal to reset video position at end of media.
        self.media_player.mediaStatusChanged.connect(self.check_media_status)

        # Connect the media player's state changed signal to change the action text
        self.media_player.stateChanged.connect(self.update_play_pause_action_text)

        # Connect the playlist's signal to change the video
        self.playlist.itemClicked.connect(self.change_video) #clicking the file
        self.playlist.itemActivated.connect(self.change_video) #activating the file with 'enter'

        # Create the menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")

        # Add actions to the file menu
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O") #add ctrl+o shortcut to open file 
        open_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_action)

        # Add keyboard shortcuts
        QShortcut(QKeySequence(Qt.Key_Space), self, self.toggle_play_pause) #play-pause spacebar toggle
        QShortcut(QKeySequence(Qt.Key_S), self, self.media_player.stop) #stop video with 'S'
        QShortcut(QKeySequence(Qt.Key_BracketLeft), self, self.decrease_speed) #decrease speed with 'down'
        QShortcut(QKeySequence(Qt.Key_BracketRight), self, self.increase_speed) #increase speed with 'up'
        QShortcut(QKeySequence(Qt.Key_Right), self, self.fast_forward) #fast forward video with 'right'
        QShortcut(QKeySequence(Qt.Key_Left), self, self.rewind) #rewind video with 'left'
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_BracketRight), self, self.next_video)  # next video with 'Ctrl+right'
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_BracketLeft), self, self.prev_video)  # previous video with 'Ctrl+left'
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_A),self,self.toggle_auto_play_next)



    ##FUNCTIONS BELOW

    #function to open video files in directories and their subdirectories and put them in a playlist
    def open_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Open Directory")
        if dir_name:
            # Find all video files in the directory and its subdirectories
            for root, dirs, files in os.walk(dir_name):
                for file_name in files:
                    if file_name.endswith((".mp4", ".mov", ".mkv", ".flv", ".ts")):  # Add other video formats as needed
                        absolute_path = os.path.join(root, file_name)

                        # Create a playlist item with up to two directories and the file name
                        playlist_item = "/".join(absolute_path.split("/")[-3:])
                        
                        # Only add new item if it's not already in the playlist
                        if playlist_item not in self.file_paths:
                            self.file_paths[playlist_item] = absolute_path  # Add the absolute path to the dictionary
                            self.playlist.addItem(playlist_item)
    
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
                self.next_video()
                self.media_player.play()

    # resizes the video to the resolution of the file defined by its meta data
    def resize_to_video(self):
        if self.media_player.isVideoAvailable():
            video_size = self.media_player.metaData("Resolution")
            self.resize(video_size)

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

    # Change to next item in the playlist - call change_video to change the video.
    def next_video(self):
        current_row = self.playlist.currentRow()
        if current_row < self.playlist.count() - 1:
            self.playlist.setCurrentRow(current_row + 1)
            self.change_video(self.playlist.currentItem())

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
        self.position_label.setText(f"Time:    {self.format_time(position)}    /") #update the position label on position change

    # Update the range of the slider when the video duration changes (like when a new video is selected)
    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
        self.duration_label.setText(self.format_time(duration)) #update the duration label on duration change

    def format_time(self, millis):
        formatted_time = str(timedelta(milliseconds=millis))
        seconds_index = formatted_time.find('.')
        if seconds_index != -1:  # If there are decimal places
            formatted_time = formatted_time[:seconds_index+2]  # Only keep one decimal place
        return formatted_time



if __name__ == "__main__":
    app = QApplication([])
    window = VideoWindow()
    window.show()
    app.exec_()