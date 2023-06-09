from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QApplication, QWidget, QListWidget, QComboBox, QDialog, QLayout, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QCheckBox, QSpacerItem
from PySide2.QtCore import Qt
import videoFunctions


#subclassing QVideoWidget for click play-pause
class ClickableVideoWidget(QVideoWidget):
    def __init__(self, video_window):
        super().__init__(video_window)
        self.video_window = video_window

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            videoFunctions.toggle_play_pause(self.video_window)  # pass parent to the function
            event.accept()
        else:
            super().mousePressEvent(event)


#subclassing the QListWidget for 'del' key shortcut to remove playlist items
class MyListWidget(QListWidget):
    def __init__(self, video_window, parent=None):
        super().__init__(parent)
        self.video_window = video_window
        self.undo_stack = []

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            action = videoFunctions.remove_current_item(self,self.video_window.file_paths, self.video_window.file_data)
            if action:
                self.undo_stack.append(action)   
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            videoFunctions.undo(self, self.video_window.file_paths,self.video_window.file_data, self.undo_stack)    
        else:
            super().keyPressEvent(event)

#class for filter dialog box creation
class FilterDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(FilterDialog, self).__init__(*args, **kwargs)
        
    
        filter_selection_layout = QGridLayout()
        filter_selection_layout.setSpacing(15)
        filter_selection_layout.setContentsMargins(5,5,5,5)
        filter_selection_layout.setSizeConstraint(QLayout.SetFixedSize) #only take up as much space as necessary to display its contents


        # play_type filter layout - to be placed in a final central widget
        play_type_layout = QVBoxLayout()
        play_type_layout.setSpacing(0) # This will reduce the space between widgets in the layout
        label = QLabel("<b><u>Play Type</b></u>")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        play_type_layout.addWidget(label, alignment=Qt.AlignTop) # Add label widget to top of box layout
        play_type_layout.setContentsMargins(5, 5, 5, 5)  # left, top, right, bottom margins

        play_type_layout.addStretch()# Add stretchable space before the widget
        
        self.play_type_selectors = {}

        button_set_widget = QWidget() # Create a widget  to store the button layout
        button_set_layout = QGridLayout() # Create a grid layout for our buttons based on possession
        button_set_layout.setContentsMargins(0, 0, 0, 0)
        button_set_layout.setVerticalSpacing(0) # This will reduce the vertical space between widgets in the layout
        button_set_layout.setVerticalSpacing(0) # This will reduce the vertical space between widgets in the layout


        possession_labels = ['BO', 'NZR', 'NZA', 'OZA']
        non_possession_labels = ['DZC', 'NZB', 'NZF', 'OZF']
        
        for i, label in enumerate(possession_labels):
            btn = QCheckBox(label)
            btn.setCheckable(True)
            button_set_layout.addWidget(btn, 0, i)
            self.play_type_selectors[label]=btn #add button to dictoinary of play type buttons
       
        
        
        for i, label in enumerate(non_possession_labels):
            btn = QCheckBox(label)
            btn.setCheckable(True)
            button_set_layout.addWidget(btn, 2, i % 4)
            self.play_type_selectors[label]=btn #add button to dictoinary of play type buttons
        
        button_set_widget.setLayout(button_set_layout) # Set the widget to the button layout

        play_type_layout.addWidget(button_set_widget, alignment=Qt.AlignTop) # Add the button widget after the label widget
        
        play_type_layout.addStretch() # Add stretchable space after the widget

        filter_selection_layout.addLayout(play_type_layout, 0, 0) #Add the play type layout to the tagging section        


        # line Rush filter layout
        all_rush_layout = QVBoxLayout()
        all_rush_layout.setSpacing(0) # This will reduce the space between widgets in the layout
        label = QLabel("<b><u>Line Rushes</b></u>")
        label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        all_rush_layout.addWidget(label, alignment=Qt.AlignTop)

        self.line_rush_selectors ={} # Store references to the shortcuts to instance variable

        
        button_set_layout = QGridLayout() #create a layout to hold rushes and opp rushes
        button_set_layout.setContentsMargins(5,5,5,5)

        rush_widget = QWidget() #create a rush widget
        rush_layout = QGridLayout() #create the rush layout
        rush_layout.setSpacing(10)  # Adjust this value to set the desired spacing
        rush_layout.setContentsMargins(5, 5, 5, 5)  # Adjust these values as desired
        rush_layout.addWidget(QLabel("<b>For : </b>")) #add for rush label

        rush_labels = ['us', 'them']
        for i, label in enumerate(rush_labels): #add widgets to the rush layout
            combo = QComboBox()
            combo.setMinimumWidth(75)
            combo.setMaximumWidth(100)
            combo.addItem('N/A')
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

        rush_widget.setLayout(rush_layout) #set the layout to the widgets we created

        opp_rush_widget = QWidget()
        opp_rush_layout = QGridLayout()
        opp_rush_layout.setSpacing(10)  # Adjust this value to set the desired spacing
        opp_rush_layout.setContentsMargins(5, 5, 5, 5)  # Adjust these values as desired
        opp_rush_layout.addWidget(QLabel("<b>Opp :</b>")) #add opponent rush label, against 
         
        opp_rush_labels = ['us', 'them']
        for i, label in enumerate(opp_rush_labels):
            combo = QComboBox()
            combo.setMinimumWidth(75)
            combo.setMaximumWidth(100)
            combo.addItem('N/A')
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
            
        opp_rush_widget.setLayout(opp_rush_layout)

        button_set_layout.addWidget(rush_widget) #add rush widget to layout
        button_set_layout.addWidget(opp_rush_widget) #add opp rush widget to layout

        button_set_widget = QWidget() #create a widget to add underneath our label
        button_set_widget.setLayout(button_set_layout) #set the layout of the widget

        all_rush_layout.addWidget(button_set_widget) # add button widget to the QVBoxLayout underneath the label widget

        filter_selection_layout.addLayout(all_rush_layout, 0, 1)


        # play Strength filter layout
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
            combo.addItem('N/A')
            combo.addItems(['5', '4', '3'])
            checkbox = QCheckBox('NE')
            self.strength_selectors[label] = [combo,checkbox] 
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

        filter_selection_layout.addLayout(strength_layout, 0, 2)


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

        filter_selection_layout.addLayout(play_attributes_layout, 0, 3)
    
        # # Create Widget to add the filter selection layout 
        # filter_selection_widget = QWidget()
        # filter_selection_widget.setLayout(filter_selection_layout)

        # Set filter_selection_layout as the layout for FilterDialog
        self.setLayout(filter_selection_layout)


        # Reuse your interface for tagging the videos here.
        # You'll have to make some modifications to ensure it works for filter selection instead of video tagging.

    # # You will need to add some method here to collect the filter criteria from the user interface.
    # def get_filter_criteria(self):
    #     # For play_type, we're checking which checkboxes are checked.
    #     play_type = {}
    #     for play in self.play_type_selectors:
    #         play_type[play] = self.play_type_selectors[play].isChecked()
        
    #     # For line_rushes, we're getting the current text in each combo box.
    #     line_rushes = {}
    #     for rush_type in self.line_rush_selectors:
    #         line_rushes[rush_type] = {rush: self.line_rush_selectors[rush_type][rush].currentText() for rush in self.line_rush_selectors[rush_type]}
            
    #     # For strength, we're getting the current text in each combo box and the checked status of each checkbox.
    #     strength = {}
    #     for strength_type in self.strength_selectors:
    #         strength[strength_type] = [self.strength_selectors[strength_type][0].currentText(), self.strength_selectors[strength_type][1].isChecked()]
            
    #     # For scoring chances, we're getting the current text in each combo box.
    #     scoring_chances = {}
    #     for chance in self.scoring_chance_selectors:
    #         scoring_chances[chance] = self.scoring_chance_selectors[chance].currentText()
            
    #     # For play_attributes, we're checking which checkboxes are checked.
    #     attributes = {}
    #     for attr in self.play_attribute_selectors:
    #         attributes[attr] = self.play_attribute_selectors[attr].isChecked()

    #     # Combining all data in a single dictionary
    #     filter_criteria = {
    #         'play_type': play_type,
    #         'line_rushes': line_rushes,
    #         'strength': strength,
    #         'scoring_chances': scoring_chances,
    #         'attributes': attributes
    #     }
    #     return filter_criteria


if __name__ == "__main__":
    app = QApplication([])
    
    dialog = FilterDialog()
    dialog.show()

    app.exec_()
