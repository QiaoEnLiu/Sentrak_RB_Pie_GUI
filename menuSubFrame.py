#zh-tw

# menuSubFrame.py
# 些程式碼為選單畫面：當Snetrak_Raspberry_GUI.py的功能選單的四個按鈕（設定、校正、記錄、識別）偵測到點擊事件時，所執行的程式碼並將子畫面刷新為清單畫面

import os, sys, base64

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QByteArray
from PyQt5.QtGui import QFont, QPixmap, QImage

from testEndFrame import testEndFrame
from id_Frame import id_LogIn_Frame
from img_to_base64 import image_to_base64

class menuSubFrame(QWidget):
    # 定義自定義信號
    # item_clicked = pyqtSignal(str, str)

    def __init__(self, title, _style, sub_pages, stacked_widget, main_window):
        super().__init__()
        self.sub_pages = sub_pages
        self.main_window = main_window
        self.stacked_widget = stacked_widget
        self.id_login_frame = id_LogIn_Frame

        self.title = title
        print(self.title)

        self.font = QFont()

        # 標題列
        title_layout = QVBoxLayout()        
        self.title_label = QLabel(self.title, self)
        # title_label.setAlignment(Qt.AlignCenter)  
        self.font.setPointSize(36)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet(_style)
        title_layout.addWidget(self.title_label)

        self.font.setPointSize(72)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 內容使用QListWidget
        self.list_widget = QListWidget(self)

        # 依功能添加列各自表項
        if self.title == '設定':
            for option in ['顯示', '警報輸出', '類比輸出', '感測器溫度保護', '診斷', '通訊', '時間', '語言']:
                self.create_list_item(option)

        elif self.title == '校正':
            for option in ['感測器校正', '大氣壓力校正', '類比輸出校正']:
                self.create_list_item(option)

        elif self.title == '記錄':
            for option in ['觀看記錄', '統計表', '下載記錄至隨身碟', '記錄方式設定']:
                self.create_list_item(option)

        elif self.title == '識別':
            for option in ['登入身份', '儀器資訊', '感測器資訊']:
                self.create_list_item(option)
        
        # 將垂直滾動條設置為不可見
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content_layout.addWidget(self.list_widget)

        # 整體佈局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(title_layout)
        main_layout.addLayout(content_layout)

        # self.main_window.logout_button.clicked.connect(self.logout_button_click)


    def create_list_item(self, option):
        # 創建 QListWidgetItem
        item = QListWidgetItem()

        # 設置圖示
        list_icon = QLabel()
        # pixmap = QPixmap('picture/test_icon.png')  # 請替換為您的實際圖示路徑
        list_icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), "picture", "test_icon.png")
        icon_base64 = image_to_base64(list_icon_path)
        icon_bytes = QByteArray.fromBase64(icon_base64.encode())
        list_icon.setPixmap(QPixmap.fromImage(QImage.fromData(icon_bytes)).scaled(72, 72))
         
        # list_icon.setPixmap(pixmap.scaled(72, 72))  # 調整大小以符合您的需求
        item_label = QLabel(option )# 設置文字
         
        # 將圖示和文字排列在一行
        layout = QHBoxLayout()

        # 將圖示和文字排列在一行，並確保沒有額外空間
        layout.setSpacing(0)
        layout.addWidget(list_icon)
        layout.addWidget(item_label)
        layout.addStretch(1)  # 添加伸縮因子
                
        # 設置項目的布局
        widget = QWidget()
        widget.setLayout(layout)

        # 將項目添加到 QListWidget
        item.setData(Qt.UserRole, option)  # 使用setData將選項存儲為UserRole
        self.list_widget.addItem(item)
        self.list_widget.setFont(self.font)
        self.list_widget.setItemWidget(item, widget)  # 將 widget 與 item 關聯起來

        # 設置點擊事件處理函數，連接點擊信號
        # self.list_widget.itemClicked.connect(self.handle_record_item_click)
        self.list_widget.itemClicked.connect(lambda item: self.handle_record_item_click(item))


    # 在 MyWindow 類別中新增一個槽函數處理 '' 頁面 item 被點擊的信號
    def handle_record_item_click(self, item):
        # 在這裡處理四個功能頁面下 item 被點擊的事件
        # 例如，切換到 testEndFrame 並顯示被點擊的項目文字
        item_text = item.data(Qt.UserRole)
        # print('子畫面：', item_text)

        # print(f"Item Clicked: {item_text} in '{self.title_label.text()}' clicked. Switching to testEndFrame.")

        # 判斷是否已經創建了 testEndFrame
        if item_text not in self.sub_pages: #"testEndFrame"
            print(item_text, item_text == '登入身份')
            if item_text == '登入身份':

                # 如果還沒有，則創建一個新的 testEndFrame
                login_frame = id_LogIn_Frame(item_text, self.title_label.styleSheet(), self.main_window)
                # 添加到堆疊中
                next_frame_index = self.stacked_widget.addWidget(login_frame)
                self.sub_pages[item_text] = next_frame_index

            else:
                # 如果還沒有，則創建一個新的 testEndFrame
                test_end_frame = testEndFrame(item_text, self.title_label.styleSheet())
                # 添加到堆疊中
                next_frame_index = self.stacked_widget.addWidget(test_end_frame)
                self.sub_pages[item_text] = next_frame_index
        else:
            # 如果已經存在，取得 下一頁（testEndFrame） 的索引
            next_frame_index = self.sub_pages[item_text]

        # 設定當前顯示的子畫面索引為 testEndFrame
        self.stacked_widget.setCurrentIndex(next_frame_index)
        self.current_page_index = next_frame_index

        print('Current Page Index:', self.current_page_index)
