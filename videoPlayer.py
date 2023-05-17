#Importing
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtCore import QUrl, QSize, Qt
from PySide2.QtGui import QKeySequence
import os

# Create a main window class
class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide2 Video Player") #title the media palyer

        # Store the current directory
        self.current_dir = None

        # Set up the media player and video widget
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()

        # Add buttons
        self.play_pause_button = QPushButton("Play")
        # self.play_button = QPushButton("Play")
        # self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")

        # Connect the buttons to the respective methods
        # self.play_button.clicked.connect(self.media_player.play)
        # self.play_button.clicked.connect(self.play_pause_button)
        # self.pause_button.clicked.connect(self.media_player.pause)
        # self.pause_button.clicked.connect(self.play_pause_button)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.stop_button.clicked.connect(self.media_player.stop)

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
        self.setCentralWidget(central_widget) #set is as central
        # central_widget.setLayout(layout) #add the layout to the central widget

        # Create a layout and add the playback widgets
        layout_box = QVBoxLayout()
        # layout.addWidget(self.video_widget) #lets move it out of layout
        layout_box.addWidget(self.play_pause_button)
        # layout_box.addWidget(self.pause_button)
        layout_box.addWidget(self.stop_button)
        # layout.addWidget(self.playlist)
        layout_box.addWidget(self.speed_slider)
        layout_box.addWidget(self.speed_label)


        # Create a splitter for the playlist and the playback buttons
        splitter = QSplitter()
        splitter.addWidget(self.playlist)
        playback_widget = QWidget()
        playback_widget.setLayout(layout_box)
        splitter.addWidget(playback_widget)
        splitter.setSizes([self.width() / 4, 3 * self.width() / 4])

        # create a main layout for the central widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget) #add video widget for the top of the box
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
        QShortcut(QKeySequence(Qt.Key_Left), self, self.decrease_speed) #decrease speed with 'left'
        QShortcut(QKeySequence(Qt.Key_Right), self, self.increase_speed) #increase speed with 'right'



    ##FUNCTIONS BELOW

       

    # function to open dialog box for selecting directory of video
    def open_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Open Directory",options=QFileDialog.DontUseNativeDialog)

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
            self.mediaPlayer.setPosition(0)

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
        else:
            self.media_player.play()
            self.play_pause_button.setText("Pause")



if __name__ == "__main__":
    app = QApplication([])
    window = VideoWindow()
    window.show()
    app.exec_()