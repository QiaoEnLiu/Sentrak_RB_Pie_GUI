#zh-tw
# testEndFrame.py

#此程式碼為子畫面最終刷新測試碼
#--第一子畫面最終測試碼執行結果 Sentrak_RaspberryPie_GUI.py -> menuSubFrame.py
#--最新最子畫面最終測試碼執行結果 menuSubFrame.py -> testEndFrame.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont


class testEndFrame(QWidget):
    def __init__(self, title, _style):
        super().__init__()
        print(title)

        font = QFont()
        
        end_label = QLabel(title, self)
        end_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        end_label.setFont(font)
        end_label.setStyleSheet(_style)

        end_sub_frame_layout = QVBoxLayout(self)
        end_sub_frame_layout.setContentsMargins(0, 0, 0, 0)
        end_sub_frame_layout.setSpacing(0) 
        end_sub_frame_layout.addWidget(end_label)