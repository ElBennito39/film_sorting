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

        # Set initial size of the window to 60% of the screen size
        screen_geometry = QDesktopWidget().screenGeometry()
        self.resize(screen_geometry.width() * 0.6, screen_geometry.height() * 0.6)

        # Set up the media player and video widget
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()

        # set the size policy
        self.video_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


        # Add buttons
        self.play_pause_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.fast_forward_button = QPushButton("Fast Forward")
        self.rewind_button = QPushButton("Rewind")

        # set the size policy
        self.play_pause_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.stop_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.fast_forward_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.rewind_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


        # Connect the playback buttons to the respective methods
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.stop_button.clicked.connect(self.media_player.stop)
        self.fast_forward_button.clicked.connect(self.fast_forward)
        self.rewind_button.clicked.connect(self.rewind)

        # Add video position slider
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

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



        # Create a central widget to anchor boxs of widgets
        central_widget = QWidget() #create central widget
        self.setCentralWidget(central_widget)#set is as central
        # central_widget.setLayout(layout) #add the layout to the central widget
    

        # Create a layout and add the playback widgets
        layout_box = QVBoxLayout()
        layout_box.addWidget(self.play_pause_button)
        layout_box.addWidget(self.stop_button)
        layout_box.addWidget(self.fast_forward_button)
        layout_box.addWidget(self.rewind_button)
        layout_box.addWidget(self.speed_slider)
        layout_box.addWidget(self.speed_label)


        # Create a splitter for the playlist and the playback buttons
        splitter = QSplitter() 
        splitter.addWidget(self.playlist) #add playlist to the split display box
        playback_widget = QWidget() #create a widget for to hold the playback buttons
        playback_widget.setLayout(layout_box) #give the button layout to the playback widget
        splitter.addWidget(playback_widget) #add playback to the split display box
        splitter.setSizes([self.width() / 4, 3 * self.width() / 4])


        # Create a splitter for duration/position labels
        split_dur_pos_labels = QSplitter()
        split_dur_pos_labels.addWidget(self.position_label)
        split_dur_pos_labels.addWidget(self.duration_label)

        #Create a splitter for the position slider and duration/position labels
        split_pos_slider = QSplitter()
        split_pos_slider.addWidget(self.position_slider)
        split_pos_slider.addWidget(split_dur_pos_labels)

        # create a main layout for the central widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget) #add video widget for the top of the box
        main_layout.addWidget(split_pos_slider)
        # main_layout.addWidget(self.position_slider) # add position slider underneath the video widget
        # main_layout.addWidget(split_dur_pos_labels) # add duration and position labels (splitter)
        main_layout.addWidget(splitter) #add the split box of playlist and playback buttons
        
        # Assign the main layout to the central widget
        central_widget.setLayout(main_layout)

        # Set the video output from media player to widget
        self.media_player.setVideoOutput(self.video_widget)

        # Connect the media player's state changed signal to handle resizing the window
        self.media_player.stateChanged.connect(self.resize_to_video)

        # Connect the media player's state signal to reset video position at end of media.
        self.media_player.mediaStatusChanged.connect(self.check_media_status)

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




    ##FUNCTIONS BELOW

       

    # function to open dialog box for selecting directory of video
    def open_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Open Directory") #,options=QFileDialog.DontUseNativeDialog)

        if dir_name:
            self.playlist.clear()
            self.current_dir = dir_name  # Store the directory name

            # Find all video files in the directory
            for file_name in os.listdir(dir_name):
                if file_name.endswith((".mp4",".mov",".mkv",".flv",".ts")):  # Add other video formats as needed
                    self.playlist.addItem(file_name)
    
    # function to change the video to be selected in the playlist
    def change_video(self, item):
        file_name = item.text()

        if file_name != '':
            # Construct the absolute path to the file
            absolute_path = os.path.join(self.current_dir, file_name)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(absolute_path)))

    # function to reset the video playback position to '0' once the media finishes playing
    def check_media_status(self, status):
        if status==QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)

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
            self.play_pause_button.setText("Play")
            # # Adjust size of central widget after changing button text
            # self.centralWidget().adjustSize()
        else:
            self.media_player.play()
            # # Adjust size of central widget after changing button text
            # self.centralWidget().adjustSize()
            self.play_pause_button.setText("Pause")

    
    # Fast forwards the video by 3 seconds
    def fast_forward(self):
        position = self.media_player.position() + 3000  # Get the current position and add 3000 milliseconds to it
        self.media_player.setPosition(position)  # Set the new position

    # Rewinds the video by 3 seconds
    def rewind(self):
        position = self.media_player.position() - 3000  # Get the current position and subtract 3000 milliseconds from it
        self.media_player.setPosition(max(position, 0))  # Set the new position, don't go below 0

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