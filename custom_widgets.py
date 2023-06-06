from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtCore import Qt
from videoFunctions import toggle_play_pause


#subclassing QVideoWidget for click play-pause
class ClickableVideoWidget(QVideoWidget):
    def __init__(self, video_window):
        super().__init__(video_window)
        self.video_window = video_window

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            toggle_play_pause(self.video_window)  # pass parent to the function
            event.accept()
        else:
            super().mousePressEvent(event)