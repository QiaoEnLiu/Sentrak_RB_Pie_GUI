#zh-tw
# testEndFrame.py

#此程式碼為子畫面最終刷新測試碼
#--第一子畫面最終測試碼執行結果 Sentrak_RaspberryPie_GUI.py -> menuSubFrame.py
#--最新最子畫面最終測試碼執行結果 menuSubFrame.py -> testEndFrame.py
try:
    import traceback
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSizePolicy, QRadioButton
    from PyQt5.QtGui import QFont
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

font = QFont()
class setUnitFrame(QWidget):
    def __init__(self, title, _style, user, stacked_widget, sub_pages):
        super().__init__()
        print(title)
        self.sub_pages=sub_pages
        
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        title_label.setFont(font)
        title_label.setStyleSheet(_style)

        temperture_label = QLabel('溫度', self)
        temperture_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(36)
        temperture_label.setFont(font)

        self.celsius_radio = QRadioButton('攝氏')
        self.fahrenheit_radio = QRadioButton('華氏')

        oxygen_label = QLabel('氧氣濃度', self)
        oxygen_label.setAlignment(Qt.AlignLeft)  
        font.setPointSize(36)
        oxygen_label.setFont(font)


        set=QPushButton('設定', self)
        set.setFont(font)
        # set.setStyleSheet(_style)
        set.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # user_label = QLabel(user.userInfo())
        # user_label.setFont(font)
        # user_label.setStyleSheet(_style)

        setUnit_layout = QVBoxLayout(self)
        setUnit_layout.setContentsMargins(0, 0, 0, 0)
        setUnit_layout.setSpacing(0) 
        setUnit_layout.addWidget(title_label)
        
        temperture_layout = QVBoxLayout(self)
        temperture_layout.setContentsMargins(0, 0, 0, 0)
        temperture_layout.setSpacing(0) 
        temperture_layout.addWidget(temperture_label)

        tempUnit_layout = QVBoxLayout()
        tempUnit_layout.addWidget(self.celsius_radio)
        tempUnit_layout.addWidget(self.fahrenheit_radio)
        temperture_layout.addLayout(tempUnit_layout)

        oxygen_layout = QVBoxLayout(self)
        oxygen_layout.setContentsMargins(0, 0, 0, 0)
        oxygen_layout.setSpacing(0)
        oxygen_layout.addWidget(oxygen_label)

        set_layout = QVBoxLayout(self)
        set_layout.setContentsMargins(0, 0, 0, 0)
        set_layout.setSpacing(0)
        set_layout.addWidget(set)

        setUnit_layout.addLayout(temperture_layout)
        setUnit_layout.addLayout(oxygen_layout)
        setUnit_layout.addLayout(set_layout)
        
        # setUnit_layout.addWidget(user_label)

        print('顯示溫度測試畫面：', title)

        self.stacked_widget = stacked_widget
        end_frame_index = self.stacked_widget.addWidget(self)
        self.current_page_index = end_frame_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print('Current Page Index:', self.current_page_index)