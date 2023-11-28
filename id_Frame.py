#zh-tw

# id_Frame.py

#此程式碼為「識別」底下「登入身份」程式碼
#--「登入身份」為id_LogIn_Fram
#--「感測器資訊」暫時進入testEndFrame.py

from PyQt5 import QtCore

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton
from PyQt5.QtGui import QFont
# from Sentrak_RaspberryPie_GUI import MyWindow


class id_LogIn_Frame(QWidget):
    login_successful = pyqtSignal(bool)

    def __init__(self, title, _style, main_window):
        super().__init__()
        print('進入畫面：', title)

        font = QFont()

         # 標題列
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0) 
        title_layout.setSpacing(0)
        title_label = QLabel(title, self)
        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setAlignment(Qt.AlignTop)  
        font.setPointSize(36)
        title_label.setFont(font)
        title_label.setStyleSheet(_style)
        title_layout.addWidget(title_label)
        # title_layout.addStretch(1)

        # 帳號輸入框
        self.username_label = QLabel("帳號:", self)
        self.username_label.setFont(font)
        # self.username_label.setStyleSheet("background-color: lightblue;")
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_input = QLineEdit(self)
        self.username_input.setFont(font)
        self.username_input.setAlignment(Qt.AlignCenter)
        self.username_denial_label = QLabel("帳號錯誤！", self)
        self.username_denial_label.setFont(font)
        self.username_denial_label.setStyleSheet("color: red;")

        # 密碼輸入框
        self.password_label = QLabel("密碼:", self)
        self.password_label.setFont(font)
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_input = QLineEdit(self)
        self.password_input.setFont(font)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setEchoMode(QLineEdit.Password)  # 隱藏輸入的文字
        self.password_denial_label = QLabel("密碼錯誤！", self)
        self.password_denial_label.setFont(font)
        self.password_denial_label.setStyleSheet("color: red;")

        font.setPointSize(42)
        self.login_label = QLabel("登入成功！<p>若要重新登入，請登出再登入。", self)
        self.login_label.setFont(font)


         # 登入按鈕
        font.setPointSize(24)
        self.login_button = QPushButton("登入", self)
        self.login_button.setFont(font)
        self.login_button.clicked.connect(self.handle_login)
        
        # 水平佈局1，包含帳號標籤和輸入框
        username_layout = QVBoxLayout()
        username_layout.setContentsMargins(20, 20, 20, 20)
        username_input_layout = QHBoxLayout()
        username_denial_layout = QHBoxLayout()
        username_input_layout.addWidget(self.username_label)
        username_input_layout.addWidget(self.username_input)
        username_denial_layout.addWidget(self.username_denial_label)
        username_layout.addLayout(username_input_layout)
        username_layout.addLayout(username_denial_layout)
        

        # 水平佈局2，包含密碼標籤和輸入框
        password_layout = QVBoxLayout()
        password_layout.setContentsMargins(20, 20, 20, 20)
        password_input_layout = QHBoxLayout()
        password_denial_layout = QHBoxLayout()
        password_input_layout.addWidget(self.password_label)
        password_input_layout.addWidget(self.password_input)
        password_denial_layout.addWidget(self.password_denial_label)
        password_layout.addLayout(password_input_layout)
        password_layout.addLayout(password_denial_layout)

        loginSuccess_layout = QVBoxLayout()
        loginSuccess_layout.setContentsMargins(20, 20, 20, 20)
        loginSuccess_layout.addWidget(self.login_label)


        login_bt_layout = QHBoxLayout()
        login_bt_layout.setContentsMargins(20, 20, 20, 20)
        login_bt_layout.addWidget(self.login_button)

        # 垂直佈局，包含所有元素
        #zh-tw 以下程式碼顯示方式為title_layout高度符合他內部元件的高度，login_bt_layout高度符合他內部元件的高度並壓在最底下，而username_layout及password_layout將剩餘的高度平均分配。
        id_LogIn_frame_layout = QVBoxLayout(self)
        id_LogIn_frame_layout.setContentsMargins(0, 0, 0, 0)
        id_LogIn_frame_layout.setSpacing(0)
        id_LogIn_frame_layout.addLayout(title_layout)
        id_LogIn_frame_layout.addStretch(1)
        id_LogIn_frame_layout.addLayout(username_layout)
        id_LogIn_frame_layout.addLayout(password_layout)
        id_LogIn_frame_layout.addLayout(loginSuccess_layout)
        id_LogIn_frame_layout.addStretch(1)
        id_LogIn_frame_layout.addLayout(login_bt_layout)

        self.login_successful.connect(self.login_successful_callback)
        self.main_window = main_window  # 添加這行，將 main_window 設定為實例變數

        self.login_button.setVisible(not self.main_window.logout_button.isVisible())
        self.username_denial_label.setVisible(False)
        self.password_denial_label.setVisible(False)
        self.login_label.setVisible(False)

        self.main_window.logout_button.clicked.connect(self.logout_button_click)

        if self.main_window.logout_button.isVisible():
            self.username_label.setVisible(False)
            self.username_input.setVisible(False)
            self.password_label.setVisible(False)
            self.password_input.setVisible(False)
            self.login_label.setVisible(True)
            self.login_button.setVisible(False)
        else:
            self.username_label.setVisible(True)
            self.username_input.setVisible(True)
            self.password_label.setVisible(True)
            self.password_input.setVisible(True)
            self.login_label.setVisible(False)
            self.login_button.setVisible(True)

            
        # print("Connected handle_login_success to login_successful signal.")
        
    def login_successful_callback(self, checkLogin):
        # print('login_successful signal received in id_LogIn_Frame:', checkLogin)
        self.main_window.handle_login_success(checkLogin)

    def handle_login(self):
        # 處理登入按鈕點擊事件的邏輯
        username = self.username_input.text()
        password = self.password_input.text()
        if username != 'abc':
            self.username_denial_label.setVisible(True)
            print('帳號錯誤！')
        else:
            self.username_denial_label.setVisible(False)
            if password != 'abc':
                self.password_denial_label.setVisible(True)
                print('密碼錯誤！')
            elif password == 'abc':

                self.username_label.setVisible(False)
                self.username_input.setVisible(False)
                self.password_label.setVisible(False)
                self.password_input.setVisible(False)
                self.login_label.setVisible(True)
                self.login_button.setVisible(False)
                self.login_label.setText(username + self.login_label.text())
                self.password_denial_label.setVisible(False)
                print('正確！')
                # 信號和槽的連接信息

                loginSuccessful = True
                self.login_successful_callback(loginSuccessful)
                self.login_button.setVisible(not self.main_window.logout_button.isVisible())
                self.main_window.logout_button.clicked.connect(self.logout_button_click)

        # print(f"Username: {username}, Password: {password}")

    def logout_button_click(self):
        self.username_label.setVisible(True)
        self.username_input.setVisible(True)
        self.password_label.setVisible(True)
        self.password_input.setVisible(True)
        self.login_label.setVisible(False)
        self.login_button.setVisible(True)
        self.login_button.setVisible(not self.main_window.logout_button.isVisible())

