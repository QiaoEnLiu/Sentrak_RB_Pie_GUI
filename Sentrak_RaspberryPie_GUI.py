#zh-tw

import sys
import numpy as np
from PyQt5.QtWidgets import \
    QApplication, QMainWindow, QWidget, QStatusBar, QVBoxLayout,\
      QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame, QGridLayout,\
      QPushButton, QStackedWidget
from PyQt5.QtCore import Qt, QTimer, QDateTime, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# matplotlib.use('Qt5Agg')

# 新增一個自訂的 Matplotlib 畫布類別
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)

    def plot(self):
        # 這裡是簡單的範例，你可以根據你的數據自行調整
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        self.ax.plot(x, y)
        self.ax.set_title('Plot', fontdict={'fontsize': 32, 'fontweight': 'bold'})
        self.ax.set_xlabel('t', fontdict={'fontsize': 24, 'fontweight': 'bold'})
        self.ax.set_ylabel('ppb', fontdict={'fontsize': 24, 'fontweight': 'bold'}, rotation=0) 

        # 在這裡更新畫布
        self.draw()

class RepeatClickButton(QPushButton):
    repeated_click = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.emit_repeated_click)

    def emit_repeated_click(self):
        print("repeated_click emitted")
        self.repeated_click.emit()
    
    def update(self):
        # 實現子畫面的更新邏輯
        print('SubFrame updated!')
        super.update()
        pass

class testSubFrame(QWidget):
    def __init__(self, title):
        super().__init__()
        print(title)

        font = QFont()
        
        test_label = QLabel(title, self)
        test_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        test_label.setFont(font)

        test_sub_frame_layout = QVBoxLayout(self)
        test_sub_frame_layout.setContentsMargins(0, 0, 0, 0)
        test_sub_frame_layout.setSpacing(0) 
        test_sub_frame_layout.addWidget(test_label)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_canvas = PlotCanvas(self, width=5, height=4)

        # 設置主視窗的尺寸
        # self.setGeometry(100, 100, 1920, 1080)
        self.setFixedSize(1920, 1080)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.font = QFont()

        # 創建狀態列
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        status_bar.setGeometry(0, 0, 1920, 100)  # 設置狀態列的尺寸
        status_bar.setStyleSheet("background-color: lightgray;")  # 設置背景顏色
        status_bar.setSizeGripEnabled(False)  # 隱藏右下角的調整大小的三角形

        # 在狀態列中央加入日期時間
        self.datetime_label = QLabel(self)
        status_bar.addWidget(self.datetime_label, 1)  # 將 QLabel 加入狀態列，並指定伸縮因子為1
        self.datetime_label.setAlignment(Qt.AlignCenter)  # 文字置中
        self.font.setPointSize(36)
        self.datetime_label.setFont(self.font)

        # 更新日期時間的 QTimer
        self.update_datetime_timer = QTimer(self)
        self.update_datetime_timer.timeout.connect(self.update_datetime)
        self.update_datetime_timer.start(1000)  # 每秒更新一次

        # 更新一次日期時間，避免一開始顯示空白
        self.update_datetime()

        # 創建主畫面
        main_frame = QFrame(self)
        main_frame.setGeometry(0, 100, 960, 780)
        main_frame.setStyleSheet("background-color: white;")  # 主畫面背景顏色
        main_label = QLabel("O<sub>2</sub>： 12.56 ppb<br>T： 16.8 °C") # ° 為Alt 0176
        main_label.setAlignment(Qt.AlignCenter)  # 文字置中
        self.font.setPointSize(72)
        main_label.setFont(self.font)
        main_frame_layout = QVBoxLayout(main_frame)
        # main_frame_layout.setContentsMargins(0, 0, 0, 0)
        main_frame_layout.setSpacing(0)  # 添加這一行以消除元素之間的間距
        main_frame_layout.addWidget(main_label)

        # 創建子畫面
        self.sub_frame = QFrame(self)
        self.sub_frame.setGeometry(960, 100, 960, 780)
        self.sub_frame.setStyleSheet("background-color: lightblue;")  # 子畫面背景顏色
        # sub_label = QLabel('子畫面')
        # sub_label.setAlignment(Qt.AlignCenter)  # 文字置中
        # self.font.setPointSize(72)
        # sub_label.setFont(self.font)
        self.sub_frame_layout = QVBoxLayout(self.sub_frame)
        self.sub_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_frame_layout.setSpacing(0)  # 添加這一行以消除元素之間的間距
        self.sub_frame_layout.addWidget(self.plot_canvas) # 在子畫面中加入 Matplotlib 的畫布
        # self.sub_frame_layout.addWidget(sub_label)

        # 在 MyWindow 類別的 __init__ 方法中初始化 QStackedWidget
        self.stacked_widget = QStackedWidget(self.sub_frame)

        # 在 MyWindow 類別的 __init__ 方法中添加畫面（此處僅添加 plot 畫面）
        self.plot_page_index = self.stacked_widget.addWidget(self.plot_canvas)

        # 在 MyWindow 類別的 __init__ 方法中添加畫面（此處添加了 menu 畫面）
        self.menu_page_index = self.stacked_widget.addWidget(self.create_menu_page())

        # 在 MyWindow 類別的 __init__ 方法中設定初始顯示的畫面
        self.stacked_widget.setCurrentIndex(self.plot_page_index)

        # 將當前的畫面索引設為 plot_page_index
        self.current_page_index = self.plot_page_index

        # 在 MyWindow 類別中添加 sub_pages 作為成員變數
        self.sub_pages = {}


        # 將QStackedWidget添加到sub_frame佈局
        self.sub_frame_layout.addWidget(self.stacked_widget)

        # 在子畫面中加入 Matplotlib 的畫布
        # self.sub_frame_layout.addWidget(self.plot_canvas)

        # 在MyWindow的__init__方法中初始化QStackedWidget和添加畫面
        # self.stacked_widget = None
        # self.current_page_index = 0  # 初始設定為主畫面的索引

        # 創建功能列
        function_bar = QFrame(self)
        function_bar.setGeometry(0, 880, 1920, 200)  # 設置功能列的尺寸
        function_bar.setStyleSheet("background-color: lightgray;")  # 設置背景顏色

        # 創建一個放置元件的頂層佈局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 消除佈局的邊距
        layout.setSpacing(0)

        # 添加狀態列到佈局
        layout.addWidget(status_bar, 1)  # 狀態列佔用 1 的高度

        # 創建一個放置元件的子佈局
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(0)

        # 添加主畫面到佈局
        grid_layout.addWidget(main_frame, 1)  # 第二個參數是優先級，表示佔用100的寬度

        # 添加子畫面到佈局
        grid_layout.addWidget(self.sub_frame, 1)

        # 添加子佈局到佈局
        layout.addLayout(grid_layout,8)

        # 添加功能列到佈局
        layout.addWidget(function_bar, 2)  # 功能列佔用 2 的高度

        # 在功能列中添加按鈕
        save_button = RepeatClickButton('資料儲存', function_bar)
        lock_label = QLabel('螢幕鎖',function_bar)
        self.menu_button = RepeatClickButton('選單', function_bar)
        self.return_button = RepeatClickButton('返回', function_bar)

        # 設定按鈕大小
        button_width, button_height = 200, 200

        save_button.setFixedSize(button_width, button_height)
        # lock_label.setFixedSize(button_width, button_height)
        self.menu_button.setFixedSize(button_width, button_height)
        self.return_button.setFixedSize(button_width, button_height)
        
        self.font.setPointSize(36)
        save_button.setFont(self.font)
        lock_label.setFont(self.font)
        self.menu_button.setFont(self.font)
        self.return_button.setFont(self.font)

        # 設定圖片路徑，picture資料夾和程式碼同一個資料夾中
        lock_icon_path = 'picture/lock_icon.png'
        lock_pixmap = QPixmap(lock_icon_path)
        lock_label.setPixmap(lock_pixmap.scaled(button_width, button_height, Qt.KeepAspectRatio))

        # 將 SpacerItem 插入按鈕之間，靠左、置中、靠右
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        function_bar_layout = QHBoxLayout(function_bar)
        function_bar_layout.addWidget(save_button)
        function_bar_layout.addItem(spacer_left)
        function_bar_layout.addWidget(lock_label)
        function_bar_layout.addItem(spacer_right)
        function_bar_layout.addWidget(self.menu_button)
        function_bar_layout.addWidget(self.return_button)

        # 在function_bar中添加選單按鈕的點擊事件
        self.menu_button.repeated_click.connect(self.switch_to_menu)
        self.return_button.repeated_click.connect(self.switch_to_previous_page)

        self.menu_button.setVisible(True)
        self.return_button.setVisible(False)

        # 顯示視窗
        self.show()

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")
        self.datetime_label.setText(formatted_datetime)

        # 新增以下兩行以更新折線圖
        self.plot_canvas.plot()
        self.plot_canvas.draw()

    # 在MyWindow類別中新增一個方法用於切換畫面
    def switch_to_menu(self):

        if self.menu_page_index is None:
            menu_page = self.create_menu_page()
            self.menu_page_index = self.stacked_widget.addWidget(menu_page)

        if self.current_page_index != self.menu_page_index:
            self.stacked_widget.setCurrentIndex(self.menu_page_index)
            self.current_page_index = self.menu_page_index

        else:
            # 如果當前已經是主選單索引，再次切換到主選單
            self.stacked_widget.setCurrentIndex(self.menu_page_index)

        # 根據當前的畫面索引顯示或隱藏按鈕
        self.menu_button.setVisible(self.current_page_index == self.plot_page_index)
        self.return_button.setVisible(self.current_page_index == self.menu_page_index)

    # 在MyWindow中新增一個方法用於創建選單畫面
    def create_menu_page(self):        
        menu_page = QFrame(self)
        menu_page.setStyleSheet("background-color: lightgreen;")  # 選單畫面背景顏色

        self.font.setPointSize(32)
        # menu_label = QLabel('選單')
        # menu_label.setAlignment(Qt.AlignCenter)  # 文字置中
        # menu_label.setFont(self.font)
        menu_page_layout = QGridLayout(menu_page)
        menu_page_layout.setSpacing(0)
        # menu_page_layout.addWidget(menu_label)

        # 將GridLayout設置為子畫面的佈局
        # self.sub_frame.setLayout(menu_page_layout)
        # menu_page.setLayout(menu_page_layout)

        # 顯示四個按鈕
        set_button = RepeatClickButton('設定', menu_page)
        calibrate_button = RepeatClickButton('校正', menu_page)
        record_button = RepeatClickButton('紀錄', menu_page)
        identify_button = RepeatClickButton('識別', menu_page)

        # 設定按鈕大小
        button_width, button_height = 300, 300

        set_button.setFixedSize(button_width, button_height)
        calibrate_button.setFixedSize(button_width, button_height)
        record_button.setFixedSize(button_width, button_height)
        identify_button.setFixedSize(button_width, button_height)

        # 設定按鈕的背景顏色，方便檢查它們的可見性
        set_button.setStyleSheet("background-color: red;")
        calibrate_button.setStyleSheet("background-color: green;")
        record_button.setStyleSheet("background-color: blue;")
        identify_button.setStyleSheet("background-color: yellow;")

        set_button.setFont(self.font)
        calibrate_button.setFont(self.font)
        record_button.setFont(self.font)
        identify_button.setFont(self.font)

        # 連接按鈕點擊事件
        # set_button.clicked.connect(lambda: self.show_sub_page('設定'))
        # calibrate_button.clicked.connect(lambda: self.show_sub_page('校正'))
        # record_button.clicked.connect(lambda: self.show_sub_page('紀錄'))
        # identify_button.clicked.connect(lambda: self.show_sub_page('識別'))

        # 連接新的信號
        set_button.repeated_click.connect(lambda: self.show_sub_page('設定'))
        calibrate_button.repeated_click.connect(lambda: self.show_sub_page('校正'))
        record_button.repeated_click.connect(lambda: self.show_sub_page('紀錄'))
        identify_button.repeated_click.connect(lambda: self.show_sub_page('識別'))

        # 將按鈕添加到GridLayout中
        menu_page_layout.addWidget(set_button, 0, 0, 1, 1)
        menu_page_layout.addWidget(calibrate_button, 0, 1, 1, 1)
        menu_page_layout.addWidget(record_button, 1, 0, 1, 1)
        menu_page_layout.addWidget(identify_button, 1, 1, 1, 1)

        return menu_page
    
     # 在 MyWindow 中新增一個方法用於返回上一個畫面

    def show_sub_page(self, page_name):
        # 隱藏選單按鈕
        self.menu_button.setVisible(False)

        # 判斷是否已經創建了該子畫面
        if page_name not in self.sub_pages:
            # 如果還沒有，則創建一個新的子畫面
            sub_page = testSubFrame(page_name)

            # 添加到堆疊中
            sub_page_index = self.stacked_widget.addWidget(sub_page)
            self.sub_pages[page_name] = sub_page_index
        else:
            # 如果已經存在，取得子畫面的索引
            sub_page_index = self.sub_pages[page_name]

            # 強制刷新子畫面
            sub_page = self.stacked_widget.currentWidget()
            sub_page.update()  # 假設您的子畫面有 update 方法

        # 設定當前顯示的子畫面索引
        self.stacked_widget.setCurrentIndex(sub_page_index)
        self.current_page_index = sub_page_index
        print('Current Page Index:', self.current_page_index)

        # 觸發標題的 print
        print('進入：', page_name)

        # 顯示返回按鈕
        self.return_button.setVisible(True)


    def switch_to_previous_page(self):
        if self.stacked_widget is not None:
            # current_widget = self.stacked_widget.currentWidget()
            # 如果當前是選單畫面，直接返回主畫面
            if self.current_page_index == self.menu_page_index:
                self.stacked_widget.setCurrentIndex(self.plot_page_index)
                self.current_page_index = self.plot_page_index
            else:
                # 清除之前的子畫面
                previous_sub_frame = self.stacked_widget.currentWidget()
                self.stacked_widget.removeWidget(previous_sub_frame)
                # self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

                # 更新當前的畫面索引
                self.current_page_index = self.stacked_widget.currentIndex()

                # 如果返回主畫面，將menu_page_index設為None
                if self.current_page_index == self.plot_page_index:
                    self.menu_page_index = None

                # 刪除已經移除的子畫面的索引
                for title, sub_page_index in list(self.sub_pages.items()):
                    if sub_page_index not in range(self.stacked_widget.count()):
                        del self.sub_pages[title]

                # 切換到更新後的畫面索引
                self.stacked_widget.setCurrentIndex(self.current_page_index)

            # 根據當前的畫面索引顯示或隱藏按鈕
            self.menu_button.setVisible(self.current_page_index == self.plot_page_index)
            self.return_button.setVisible(self.current_page_index != self.plot_page_index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())