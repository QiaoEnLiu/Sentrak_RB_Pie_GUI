#zh-tw
# deviceInFo.py

#此程式碼為「識別」底下「儀器資訊」
#--「儀器資訊」為deviceInfoFrame
#--「感測器資訊」暫時進入testEndFrame.py

try:
    
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
    from PyQt5.QtGui import QFont

    import platform, os, subprocess, re, traceback
    import psutil
    # import RPi.GPIO as GPIO

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")


class internetFrame(QWidget):
    def __init__(self, title, _style, user, stacked_widget, sub_pages):
        super().__init__()
        # print(title)
        print('測試畫面：', title)
        self.title = title
        self.sub_pages=sub_pages

        self.font = QFont()

        # 標題列
        title_layout = QVBoxLayout()        
        self.title_label = QLabel(self.title, self)
        # title_label.setAlignment(Qt.AlignCenter)  
        self.font.setPointSize(36)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet(_style)
        title_layout.addWidget(self.title_label)
        # self.font.setPointSize(72)

        # title_layout.setContentsMargins(0, 0, 0, 0)
        # title_layout.setSpacing(0)

        deviceInfo_layout = QVBoxLayout()
        # deviceInfo_layout.setContentsMargins(0, 0, 0, 0)
        # deviceInfo_layout.setSpacing(0)

        self.deviceInfo_label = QLabel()
        # title_label.setAlignment(Qt.AlignCenter)  
        self.font.setPointSize(24)
        self.deviceInfo_label.setFont(self.font)
        # self.deviceInfo_label.setStyleSheet(_style) 

        # 將 deviceInfo_label 放入 QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(self.deviceInfo_label)

        deviceInfo_layout.addWidget(scroll_area)

        # 整體佈局
        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0)
        main_layout.addLayout(title_layout)
        main_layout.addLayout(deviceInfo_layout)


        # network_info = '網路介面資訊:' + '暫未提供' + '\n'
        network_info = '網路介面資訊:' + '\n'
        for line in self.get_network_info():
            network_info += line + '\n'
        # print(network_info)


        self.deviceInfo_label.setText(network_info)

        
        # print(title ,user.userInfo())


        self.stacked_widget = stacked_widget
        deviceInfo_index = self.stacked_widget.addWidget(self)
        self.current_page_index = deviceInfo_index # 將當前的畫面索引設為 plot_page_index
        # 設定當前顯示的子畫面索引
        print('Current Page Index:', self.current_page_index)


    
    
    def get_network_info(self):
        try:
            interfaces = psutil.net_if_addrs()
            result = []
            for interface, addresses in interfaces.items():
                result.append(f' Interface: {interface}')
                for address in addresses:
                    result.append(f'   Address Family: {address.family}')
                    result.append(f'     Address: {address.address}')
                    result.append(f'     Netmask: {address.netmask}')
                    result.append(f'     Broadcast: {address.broadcast}')
            return result
        except Exception as e:
            return f'無法取得網路介面資訊: {e}'
        