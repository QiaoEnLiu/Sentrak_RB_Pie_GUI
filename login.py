#zh-tw

# login.py
# 點選解鎖案紐後顯示員工登入的訊息窗

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from userPermissions import Permissions

global_loginUser = None
class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()

        # 定義使用者字典
        self.users = {
            'GUI_Developer': {
                'username': 'asdf',
                'password': 'asdf',
                'control': True,
                'read': True,
                'download': True
            },
            'user_P001': {
                'username': 'Ayt001',
                'password': 'Priorty001',
                'control': True,
                'read': True,
                'download': True
            },
            'user_P0A1': {
                'username': 'Ayt0A1',
                'password': 'Priorty002',
                'control': True,
                'read': True,
                'download': False
            },
            'user_P0B1': {
                'username': 'Ayt0B1',
                'password': 'Priorty003',
                'control': False,
                'read': True,
                'download': False
            }
        }


        self.initUI()

    def initUI(self):
        
        font = QFont()
        font.setPointSize(36)

        self.presentUser=None

        # 帳號輸入框
        self.username_label = QLabel("帳號:", self)
        self.username_label.setFont(font)
        self.username_denial_label = QLabel(self) # "帳號錯誤！",
        self.username_denial_label.setFont(font)
        self.username_denial_label.setStyleSheet("color: red;")
        self.username_input = QLineEdit(self)
        self.username_input.setText('asdf')
        self.username_input.setFont(font)
        

        # 密碼輸入框
        self.password_label = QLabel("密碼:", self)
        self.password_label.setFont(font)
        self.password_denial_label = QLabel(self) # "密碼錯誤！",
        self.password_denial_label.setFont(font)
        self.password_denial_label.setStyleSheet("color: red;")
        self.password_input = QLineEdit(self)
        self.password_input.setText('asdf')
        self.password_input.setFont(font)
        self.password_input.setEchoMode(QLineEdit.Password)  # 隱藏輸入的文字
        

        font.setPointSize(42)
        self.login_label = QLabel(self) #"登入成功！<p>若要重新登入，請登出再登入。",
        self.login_label.setFont(font)

        # 確定按鈕
        ok_button = QPushButton('確定', self)
        ok_button.setFont(font)
        ok_button.clicked.connect(self.handle_login)

        # 取消按鈕
        cancel_button = QPushButton('取消', self)
        cancel_button.setFont(font)
        cancel_button.clicked.connect(self.reject)

        
        # 水平佈局1，包含帳號標籤和輸入框
        username_layout = QVBoxLayout()
        username_layout.setContentsMargins(20, 20, 20, 20)
        username_title_layout = QHBoxLayout()
        username_input_layout = QHBoxLayout()
        username_title_layout.addWidget(self.username_label)
        username_title_layout.addWidget(self.username_denial_label)
        username_title_layout.addStretch(1)
        username_input_layout.addWidget(self.username_input)
        username_layout.addLayout(username_title_layout)
        username_layout.addLayout(username_input_layout)
        

        # 水平佈局2，包含密碼標籤和輸入框
        password_layout = QVBoxLayout()
        password_layout.setContentsMargins(20, 20, 20, 20)
        password_title_layout = QHBoxLayout()
        password_input_layout = QHBoxLayout()
        password_title_layout.addWidget(self.password_label)
        password_title_layout.addWidget(self.password_denial_label)
        password_title_layout.addStretch(1)
        password_input_layout.addWidget(self.password_input)
        password_layout.addLayout(password_title_layout)
        password_layout.addLayout(password_input_layout)

        loginSuccess_layout = QVBoxLayout()
        loginSuccess_layout.setContentsMargins(20, 20, 20, 20)
        loginSuccess_layout.addWidget(self.login_label)


        login_bt_layout = QHBoxLayout()
        login_bt_layout.setContentsMargins(20, 20, 20, 20)

        # 垂直佈局，包含所有元素
        id_LogIn_frame_layout = QVBoxLayout(self)

        id_LogIn_frame_layout.addStretch(0)
        id_LogIn_frame_layout.addLayout(username_layout)
        id_LogIn_frame_layout.addLayout(password_layout)
        id_LogIn_frame_layout.addStretch(1)
        id_LogIn_frame_layout.addWidget(ok_button)
        id_LogIn_frame_layout.addWidget(cancel_button)

        self.setLayout(id_LogIn_frame_layout)
        self.setWindowTitle('員工登入')

        # 設置對話框大小
        self.setFixedSize(960, 560)

    def handle_login(self): #讀取字典
        # 獲取輸入的帳號和密碼
        username = self.username_input.text()
        password = self.password_input.text()
        global global_loginUser
        


        # 檢查使用者是否存在
        if any('username' in user_info and user_info['username'] == username and user_info['password'] == password for user_info in self.users.values()):
            # print('輸入的帳號：', username)
            # print('輸入的密碼：', password)
            user_info = next(user_info for user_info in self.users.values() if user_info['username'] == username)
            user_permissions = {k: v for k, v in user_info.items() if k in ['username', 'password', 'control', 'read', 'download']}
            self.presentUser = Permissions(**user_permissions)
            # print('self.presentUser:',self.presentUser.userInfo())
            global_loginUser = self.presentUser
            QMessageBox.information(self, '登入成功', f'歡迎{username}使用')
            # print('login.py:',global_loginUser.userInfo())
            self.accept()
        else:
            self.presentUser = None
            global_loginUser = self.presentUser
            # print('輸入的帳號：', username)
            # print('輸入的密碼：', password)
            # print('存在的使用者：', list(self.users.keys()))
            QMessageBox.critical(self, '登入失敗', '帳號密碼錯誤！')


    # def handle_login(self): #套用類別
    #     global global_loginUser
    #     username = self.username_input.text()
    #     password = self.password_input.text()
    #     print('帳號:', username)
    #     print('密碼:', password)
    #     successLoginInfo='歡迎{}使用'.format(username)     

    #     # Permissions(帳號, 密碼, 
    #     #             控制（設定）, 讀取（預覽）, 下載（讀取資料檔案）)

    #     user0=Permissions(username='asdf', password='asdf',
    #                        control=True, read=True, download=True)
        
    #     user_P001=Permissions(username='Ayt001', password='Priorty001',
    #                        control=True, read=True, download=True)
        
    #     user_P0A1=Permissions(username='Ayt0A1', password='Priorty002',
    #                        control=True, read=True, download=False)
        
    #     user_P0B1=Permissions(username='Ayt0B1', password='Priorty003',
    #                        control=False, read=True, download=False)

    #     # 這裡模擬登入的邏輯，實際上您需要替換成真實的帳號密碼驗證邏
    #     # 登入成功、失敗的情況
    #     if username == user0.username and password == user0.password:
    #         # 登入成功，執行 accept() 以關閉對話框
    #         self.presentUser=user0
    #         global_loginUser = self.presentUser
    #         QMessageBox.information(self, '登入成功', successLoginInfo)
    #         print(global_loginUser.userInfo())
    #         # print(user0.username, ' '+str(user0.control), ' '+str(user0.read), ' '+ str(user0.download), sep='\n')
    #         self.accept()

    #     elif username == user_P001.username and password == user_P001.password:
    #         # 登入成功，執行 accept() 以關閉對話框
    #         self.presentUser=user_P001
    #         global_loginUser = self.presentUser
    #         QMessageBox.information(self, '登入成功', successLoginInfo)
    #         print(global_loginUser.userInfo())
    #         # print(user_P001.username, ' '+str(user_P001.control), ' '+str(user_P001.read), ' '+ str(user_P001.download), sep='\n')
    #         self.accept()

    #     elif username == user_P0A1.username and password == user_P0A1.password:
    #         # 登入成功，執行 accept() 以關閉對話框
    #         self.presentUser=user_P0A1
    #         global_loginUser = self.presentUser
    #         QMessageBox.information(self, '登入成功', successLoginInfo)
    #         print(global_loginUser.userInfo())
    #         # print(user_P0A1.username, ' '+str(user_P0A1.control), ' '+str(user_P0A1.read), ' '+ str(user_P0A1.download), sep='\n')
    #         self.accept()

    #     elif username == user_P0B1.username and password == user_P0B1.password:
    #         # 登入成功，執行 accept() 以關閉對話框
    #         self.presentUser=user_P0B1
    #         global_loginUser = self.presentUser
    #         QMessageBox.information(self, '登入成功', successLoginInfo)
    #         print(global_loginUser.userInfo())
    #         # print(user_P0B1.username, ' '+str(user_P0B1.control), ' '+str(user_P0B1.read), ' '+ str(user_P0B1.download), sep='\n')
    #         self.accept()

    #     elif username == '' or password == '':
    #         self.presentUser=None
    #         global_loginUser = self.presentUser
    #         QMessageBox.critical(self, '登入失敗', '請輸入帳號密碼！')

    #     else:
    #         self.presentUser=None
    #         global_loginUser = self.presentUser
    #         # 顯示錯誤提示，並保持對話框打開
    #         QMessageBox.critical(self, '登入失敗', '帳號密碼錯誤！')
    #         print('Login Fail')

    def get_global_loginUser(self):
        return global_loginUser
