from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QListWidget
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
            action = videoFunctions.remove_current_item(self,self.video_window.file_paths)
            if action:
                self.undo_stack.append(action)   
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            videoFunctions.undo(self, self.video_window.file_paths, self.undo_stack)    
        else:
            super().keyPressEvent(event)



