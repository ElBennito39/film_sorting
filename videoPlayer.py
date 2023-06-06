""" 
PySide2 Video Application for the review of hockey film.

author: Brien Bennett
website: BennettHockey.com

Application will:
    facilitate video playback, 
    tagging of hockey meta data to video files via the comments section of .mp4 metadata.
    filtering of a playlist populated by directory selection by those meta data tags.
    

"""
#Importing
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence, QFont
import code

from datetime import timedelta
import os, json

from videoFunctions import *
from taggingFunctions import *
from custom_widgets import ClickableVideoWidget, MyListWidget

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
        self.video_widget = ClickableVideoWidget(self) ## custom subclass from 'clicking' window

        # Set the size policy
        self.video_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        # Set a minimum size for the video widget
        self.video_widget.setMinimumSize(500, 400)

        # Create QActions for playback functionality
        self.stop_action = QAction("Stop", self)
        self.fast_forward_action = QAction("Fast Forward", self)
        self.rewind_action = QAction("Rewind", self)
        self.next_action = QAction('Next', self)
        self.prev_action = QAction('Previous', self)

        # Connect the playback actions to the respective methods
        self.stop_action.triggered.connect(self.media_player.stop)
        # self.fast_forward_action.triggered.connect(self.fast_forward)
        self.fast_forward_action.triggered.connect(lambda: fast_forward(self))
        self.rewind_action.triggered.connect(lambda: rewind(self))
        self.next_action.triggered.connect(lambda: next_video(self))
        self.prev_action.triggered.connect(lambda: prev_video(self))
        
        # Create QToolButton so we can control the size of play-pause function interfacte
        self.play_pause_button = QToolButton()
        self.play_pause_button.setText("Play")
        
        # Connect the play pause button to the respective method
        self.play_pause_button.clicked.connect(lambda: toggle_play_pause(self))
        self.play_pause_button.setFixedWidth(self.play_pause_button.fontMetrics().horizontalAdvance('Pause') + 20)

        # Create a checkbox for auto-play next
        self.auto_play_next_checkbox = QCheckBox("Auto-Next")
        self.auto_play_next_checkbox.stateChanged.connect(lambda state: set_auto_play_next(self, state))

        # Store the auto-play next setting
        self.auto_play_next = False

        # Create a checkbox for tagging tool visibility
        self.tag_vis_checkbox = QCheckBox("Tagging Tools")
        self.tag_vis_checkbox.stateChanged.connect(lambda: toggle_widget_visibility(tagging_widget)) #connect the click of the box to the function for visibility


        # Create speed slider selection
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(2)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(10)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksAbove)
        self.speed_slider.valueChanged.connect(lambda value: change_speed(self,value))
        self.speed_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.speed_slider.setStyleSheet("""

            QSlider::groove:horizontal {
                height: 2px; /* Change the height as you wish */
                border: 1px solid #999999;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 1px 0;
            }

            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 8px solid #5c5c5c;
                width: 10px;
                margin: -2px 0; /* handle is positioned by default on the contents rect of the groove. Expand outside the groove */
                border-radius: 10px;
            }
            """)

        # Create a label for playback speed
        self.speed_label = QLabel()

        # Create a layout for the speed slider and label
        speed_section = QHBoxLayout()
        speed_section.setSpacing(10)  # Adjust the value as needed
        speed_section.setContentsMargins(5, 5, 5, 5)  # Adjust the values as needed
        speed_section.addWidget(self.speed_slider)
        speed_section.addWidget(self.speed_label)
        speed_widget = QWidget()
        speed_widget.setLayout(speed_section)
        speed_widget.setMaximumHeight(75) # Set maximum heights for the widget


        # Create a toolbar and add the buttons, actions, checkbox, and speed slider
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
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.tag_vis_checkbox)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addWidget(QLabel("<html><b>Video Speed:</b></html>"))
        self.toolbar.addSeparator()
        self.toolbar.addWidget(speed_widget)
        self.toolbar.setMaximumHeight(42)

        # Add video position slider
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(lambda position: set_position(self, position))
        self.position_slider.setFixedHeight(20)
        self.position_slider.setStyleSheet("""

            QSlider::groove:horizontal {
                height: 2px; /* Change the height as you wish */
                border: 1px solid #999999;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }       
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 10px solid #5c5c5c;
                width: 15px;
                margin: -2px 0; /* handle is positioned by default on the contents rect of the groove. Expand outside the groove */
                border-radius: 25px;
            }
            """)


        # Add labels for video position and duration
        self.position_label = QLabel()
        self.position_label.setMaximumHeight(40)
        self.position_label.setFont(QFont(str(self.position_label.font()),7))
        self.duration_label = QLabel()
        self.duration_label.setMaximumHeight(40)
        self.duration_label.setFont(QFont(str(self.duration_label.font()),7))

        # Connect the media player's positionChanged and durationChanged signals
        self.media_player.positionChanged.connect(lambda position: position_changed(self, position))
        self.media_player.durationChanged.connect(lambda duration: duration_changed(self, duration))
        
        # Create playlist widget
        self.playlist = MyListWidget(self)
        self.playlist.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.playlist.setSelectionMode(QAbstractItemView.ExtendedSelection) # allow multiple item selection


        ### Window Layout ###

        # Create a central widget to anchor boxes of widgets
        central_widget = QWidget() #create central widget
        self.setCentralWidget(central_widget)#set is as central

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)  # This sets the spacing between widgets to 5 pixels
        main_layout.setContentsMargins(5, 2, 5, 2)  # This sets the margins on the left, top, right, and bottom to 5 pixels

        #Create a label to display the file path
        self.file_path_label = QLabel()  # File path label
        
        #Add the file path label to the main layout
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
        position_widget.setMaximumHeight(75) # Set maximum heights for the widget

        # Add the position_section layout to the main layout
        main_layout.addWidget(position_widget)

        # Add tool bar to main layout
        main_layout.addWidget(self.toolbar)

        # Create a layout for meta data tagging, will contain multiple sections of tagging interactions
        tagging_section = QGridLayout()
        tagging_section.setSpacing(15)
        tagging_section.setContentsMargins(5,5,5,5)
        tagging_section.setSizeConstraint(QLayout.SetFixedSize) #only take up as much space as necessary to display its contents

        # Far left: Play-type tagging interactions
        play_type_layout = QVBoxLayout()
        play_type_layout.setSpacing(0) # This will reduce the space between widgets in the layout
        label = QLabel("<b><u>Play Type</b></u>")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        play_type_layout.addWidget(label, alignment=Qt.AlignTop) # Add label widget to top of box layout
        play_type_layout.setContentsMargins(5, 5, 5, 5)  # left, top, right, bottom margins

        play_type_layout.addStretch()# Add stretchable space before the widget

        button_set_widget = QWidget() # Create a widget  to store the button layout

        button_set_layout = QGridLayout() # Create a grid layout for our buttons based on possession
        button_set_layout.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom margins
        # button_set_layout.setSpacing(5) # This will reduce the space between widgets in the layout
        button_set_layout.setVerticalSpacing(0) # This will reduce the vertical space between widgets in the layout
        
        possession_labels = ['BO', 'NZR', 'NZA', 'OZA']
        non_possession_labels = ['DZC', 'NZB', 'NZF', 'OZF']
        self.play_type_selectors = {}  # Store references to the shortcuts to instance variable
        shortcuts = ['q', 'w', 'e', 'r', 'a', 's', 'd', 'f']  # Keyboard shortcuts
        
        for i, label in enumerate(possession_labels):
            btn = QPushButton(label)
            btn.setCheckable(True)
            button_set_layout.addWidget(btn, 0, i)
            self.play_type_selectors[label]=btn #add button to dictoinary of play type buttons
            shortcut = QShortcut(QKeySequence(shortcuts[i]), button_set_widget)
            shortcut.activated.connect(btn.click)  # Connect shortcut to button click
            
        for i, label in enumerate(non_possession_labels):
            btn = QPushButton(label)
            btn.setCheckable(True)
            button_set_layout.addWidget(btn, 1, i % 4)
            self.play_type_selectors[label]=btn #add button to dictoinary of play type buttons
            shortcut = QShortcut(QKeySequence(shortcuts[i+len(possession_labels)]), button_set_widget)
            shortcut.activated.connect(btn.click)  # Connect shortcut to button click

        button_set_widget.setLayout(button_set_layout) # Set the widget to the button layout

        play_type_layout.addWidget(button_set_widget, alignment=Qt.AlignTop) # Add the button widget after the label widget
        
        play_type_layout.addStretch() # Add stretchable space after the widget
        
        tagging_section.addLayout(play_type_layout, 0, 0) #Add the play type layout to the tagging section        

        # Center left: line Rush attributes tagging interactions
        all_rush_layout = QVBoxLayout()
        all_rush_layout.setSpacing(0) # This will reduce the space between widgets in the layout
        label = QLabel("<b><u>Line Rushes</b></u>")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        all_rush_layout.addWidget(label, alignment=Qt.AlignTop)
        
        button_set_layout = QGridLayout() #create a layout to hold rushes and opp rushes
        button_set_layout.setContentsMargins(5,5,5,5)

        self.line_rush_selectors ={} # Store references to the shortcuts to instance variable

        rush_layout = QGridLayout() #create the rush layout
        rush_layout.setSpacing(10)  # Adjust this value to set the desired spacing
        rush_layout.setContentsMargins(5, 5, 5, 5)  # Adjust these values as desired
        rush_layout.addWidget(QLabel("<b>For : </b>")) #add for rush label
        rush_labels = ['us', 'them']
        for i, label in enumerate(rush_labels): #add widgets to the rush layout
            combo = QComboBox()
            combo.setMinimumWidth(75)
            combo.setMaximumWidth(100)
            combo.addItem('0')
            combo.addItems([str(n) for n in range(1, 6)])
            if 'rush_for' not in self.line_rush_selectors: #create the sub-dictionary if it doesn't exist
                self.line_rush_selectors['rush_for'] = {}
            self.line_rush_selectors['rush_for'][label] = combo #add dictionary of rush label and the combo box value to the video class instance variable self.combo_boxes
            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter) # Align the label to the center
            rush_layout.addWidget(label_widget, 0, i * 2 + 1)  # Adjust the column index
            rush_layout.addWidget(combo, 1, i * 2 + 1)  # Adjust the column index
            
            # Add "vs." label
            if i < len(rush_labels) - 1:
                vs_label = QLabel("vs.")
                vs_label.setAlignment(Qt.AlignCenter)
                vs_label.setFixedWidth(35)
                rush_layout.addWidget(vs_label, 1, i * 2 + 2)  # Adjust the column index

        rush_widget = QWidget() #create a rush widget
        rush_widget.setLayout(rush_layout) #set the layout to the widgets we created

        opp_rush_layout = QGridLayout()
        opp_rush_layout.setSpacing(10)  # Adjust this value to set the desired spacing
        opp_rush_layout.setContentsMargins(5, 5, 5, 5)  # Adjust these values as desired
        opp_rush_layout.addWidget(QLabel("<b>Opp :</b>")) #add opponent rush label, against  
        opp_rush_labels = ['us', 'them']
        for i, label in enumerate(opp_rush_labels):
            combo = QComboBox()
            combo.setMinimumWidth(75)
            combo.setMaximumWidth(100)
            combo.addItem('0')
            combo.addItems([str(n) for n in range(1, 6)])
            if 'rush_opp' not in self.line_rush_selectors: # create the sub-dictionary if doesn't exist
                self.line_rush_selectors['rush_opp'] = {}
            self.line_rush_selectors['rush_opp'][label] = combo
            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter) # Align the label to the center
            opp_rush_layout.addWidget(label_widget, 0, i * 2 + 1)  # Adjust the column index
            opp_rush_layout.addWidget(combo, 1, i * 2 + 1)  # Adjust the column index
            
            # Add "vs." label
            if i < len(rush_labels) - 1:
                vs_label = QLabel("vs.")
                vs_label.setFixedWidth(35)
                vs_label.setAlignment(Qt.AlignCenter)
                opp_rush_layout.addWidget(vs_label, 1, i * 2 + 2)  # Adjust the column index
            
        opp_rush_widget = QWidget()
        opp_rush_widget.setLayout(opp_rush_layout)
        
        button_set_layout.addWidget(rush_widget) #add rush widget to layout
        button_set_layout.addWidget(opp_rush_widget) #add opp rush widget to layout

        button_set_widget = QWidget() #create a widget to add underneath our label
        button_set_widget.setLayout(button_set_layout) #set the layout of the widget

        all_rush_layout.addWidget(button_set_widget) # add button widget to the QVBoxLayout underneath the label widget

        tagging_section.addLayout(all_rush_layout, 0, 1)


        # Center right: play Strength attributes tagging interactions
        strength_layout = QVBoxLayout()
        strength_layout.setSpacing(5) # This will reduce the space between widgets in the layout
        label = QLabel("<b><u>Strength</b></u>")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        strength_layout.addWidget(label, alignment=Qt.AlignTop)
        strength_layout.setContentsMargins(5, 5, 5, 5)  # left, top, right, bottom margins

        self.strength_selectors = {}
        button_set_layout = QGridLayout() #create a grid layout for strength dropdown boxes
        button_set_layout.setSpacing(0)
        button_set_layout.setContentsMargins(5, 5, 5, 5)  # left, top, right, bottom margins
        strength_labels = ['for', 'opp']
        for i, label in enumerate(strength_labels):
            combo = QComboBox()
            combo.setMinimumWidth(100)
            combo.setMaximumWidth(100)
            combo.addItem('5')
            combo.addItems(['4', '3'])
            checkbox = QCheckBox('NE')
            self.strength_selectors[label] = [combo,checkbox] # TODO: this needs to record the proper/oppone, the combobox value and the state of the NE checkbox
            # label_widget = QLabel(label)
            # label_widget.setMaximumHeight(30)
            # label_widget.setContentsMargins(0,0,0,0) # Adjust the margin values as needed
            # button_set_layout.addWidget(label_widget, 0, i*2)
            button_set_layout.addWidget(combo, 0, i*2)

            # Add QLabel "on"
            if i < len(strength_labels) - 1:
                on_label = QLabel("on")
                # on_label.setFixedWidth(50)
                on_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                on_label.setAlignment(Qt.AlignCenter)
                button_set_layout.addWidget(on_label, 0, i * 2 + 1)

            button_set_layout.addWidget(checkbox, 2, i * 2)
        button_set_widget = QWidget() #create a widget for the strength downdowns
        button_set_widget.setLayout(button_set_layout) #add the dropdown layout to the widget

        strength_layout.addSpacerItem(QSpacerItem(5,5)) # put a spacer between section label and strength dropdowns
        strength_layout.addWidget(button_set_widget) #add the buttons to the section after the label

        combo_box_layout = QGridLayout()
        combo_box_layout.setSpacing(5)
        combo_box_layout.setContentsMargins(5,5,5,5)
        self.scoring_chance_selectors = {}
        combo_box_labels = ['for_chance', 'opp_chance'] #create dropdowns for scoring chances
        for i, label in enumerate(combo_box_labels):
            combo = QComboBox()
            combo.setMinimumWidth(100)
            combo.setMaximumWidth(100)
            combo.addItem("N/A")
            combo.addItems(['A', 'B', 'C'])
            self.scoring_chance_selectors[label] = combo
            combo_box_layout.addWidget(QLabel(label), i, 0) #add label to combo box
            combo_box_layout.addWidget(combo, i, 1) #add combo box to strength layout, under strength dropdowns

        combo_box_widget = QWidget()
        combo_box_widget.setLayout(combo_box_layout)

        strength_layout.addWidget(combo_box_widget)

        
        tagging_section.addLayout(strength_layout, 0, 2)


        # Far right: Play-attribute tagging interactions
        play_attributes_layout = QVBoxLayout()
        label = QLabel("<b><u>Play Attributes</b></u>")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        play_attributes_layout.addWidget(label, alignment=Qt.AlignTop)

        play_attributes_layout.addStretch()  # Add stretchable space before the widget

        self.play_attribute_selectors = {}

        button_set_layout = QGridLayout()
        attribute_labels = ['GF', 'Shots For', 'takeaway', 'drew_penalty', 'GA', 'Shots Against', 'giveaway', 'took_penalty']
        for i, label in enumerate(attribute_labels):
            checkbox = QCheckBox(label)
            self.play_attribute_selectors[label] = checkbox
            button_set_layout.addWidget(checkbox, i // 4, i % 4)
        button_set_widget = QWidget()
        button_set_widget.setLayout(button_set_layout)
        play_attributes_layout.addWidget(button_set_widget)

        play_attributes_layout.addStretch()  # Add stretchable space after the widget

        tagging_section.addLayout(play_attributes_layout, 0, 3)

        
        # Create Widget to add to main layout from the tagging_section layout
        tagging_widget = QWidget()
        tagging_widget.setLayout(tagging_section)

        # Add tagging section widget to the main layout
        main_layout.addWidget(tagging_widget)

        ##Final assignment of the central widget to the main layout
        # Assign the main layout to the central widget
        central_widget.setLayout(main_layout)


        ### Connect media and signals ###

        # Set the video output from media player to widget
        self.media_player.setVideoOutput(self.video_widget)

        # Connect the media player's state signal to reset video position at end of media.
        self.media_player.mediaStatusChanged.connect(lambda status: check_media_status(self,status))

        # Connect the media player's state changed signal to change the action text
        self.media_player.stateChanged.connect(lambda state: update_play_pause_action_text(self,state))

        # Connect the playlist's signal to change the video
        self.playlist.itemClicked.connect(lambda item: change_video(self, item)) #clicking the file
        self.playlist.itemActivated.connect(lambda item: change_video(self, item)) #activating the file with 'enter'
        # load the tagging data from the comments of the video file activated. set the tagging interface
        self.playlist.itemActivated.connect(lambda: set_from_comments(self, load_tags_from_video(self.file_path_label.text())))
        self.playlist.itemActivated.connect(lambda: set_from_comments(self, load_tags_from_video(self.file_path_label.text())) if load_tags_from_video(self.file_path_label.text()) is not None else set_default_tagging_data(self))


        ### Menu ###

        # Create the menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")

        # Add actions to the file menu
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O") #add ctrl+o shortcut to open file 
        open_action.triggered.connect(lambda: open_directory(self))
        file_menu.addAction(open_action)

        hide_tag_tools = QAction("Hide Tagging Tools", self)
        hide_tag_tools.setShortcut("Ctrl+T") #add ctrl+t shortcut to toggle tag toolbar visibility via the tag_vis_checkbox
        hide_tag_tools.triggered.connect(lambda: toggle_checkbox(self.tag_vis_checkbox))
        file_menu.addAction(hide_tag_tools)

        select_auto_next_video = QAction("Auto Play Next Video",self)
        select_auto_next_video.setShortcut("Ctrl+A") #add ctrl+A shortcut to toggle tag toolbar visibility via the tag_vis_checkbox
        select_auto_next_video.triggered.connect(lambda: toggle_auto_play_next(self))
        file_menu.addAction(select_auto_next_video)

        # #TODO: save video tags
        save_tags_action = QAction("Save Tagging Data",self)
        save_tags_action.setShortcut("Ctrl+S") #add ctrl+s shortcut to save the video tags
        save_tags_action.triggered.connect(lambda: save_tagging_data(self,self.file_path_label.text())) #connect the triggered action with the function to save the tagging 
        file_menu.addAction(save_tags_action)

        # Add keyboard shortcuts for play, pause, stop, speed, position, next, previous, auto-play next, full-screen
        QShortcut(QKeySequence(Qt.Key_Space), self, lambda: toggle_play_pause(self)) #play-pause spacebar toggle
        QShortcut(QKeySequence(Qt.Key_Shift + Qt.Key_S), self, self.media_player.stop) #stop video with 'S'
        QShortcut(QKeySequence(Qt.Key_BracketLeft), self, lambda: decrease_speed(self)) #decrease speed with 'down'
        QShortcut(QKeySequence(Qt.Key_BracketRight), self, lambda: increase_speed(self)) #increase speed with 'up'
        QShortcut(QKeySequence(Qt.Key_Right), self, lambda: fast_forward(self)) #fast forward video with 'right'
        QShortcut(QKeySequence(Qt.Key_Left), self, lambda: rewind(self)) #rewind video with 'left'
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_BracketRight), self, lambda: next_video(self))  # next video with 'Ctrl+right'
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_BracketLeft), self, lambda: prev_video(self))  # previous video with 'Ctrl+left'
        # QShortcut(QKeySequence(Qt.CTRL + Qt.Key_A),self,lambbda: toggle_auto_play_next(self))
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), self, lambda: toggle_window_size(self))
        # QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), self, lambda: toggle_checkbox(self.tag_vis_checkbox))

    def connect_signals(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    with open('stylesheet.qss', 'r') as f:
        stylesheet = f.read()

    # Set the stylesheet for the application
    app.setStyleSheet(stylesheet)

    window = VideoWindow()
    window.show()

    # # Enter the Python terminal
    # breakpoint()
    app.exec_()