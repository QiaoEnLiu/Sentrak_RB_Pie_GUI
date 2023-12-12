#zh-tw 我修正我的需求，將以下程式碼修改為讀取COM埠，而不是佔用


import minimalmodbus, serial, serial.tools.list_ports

# 取得可用的 COM 埠列表
available_ports = list(serial.tools.list_ports.comports())

# 列印每個可用的 COM 埠
for port in available_ports:
    print(f"Available Port: {port.name}")

portName=input('通訊埠：')#COM3, COM4


# 替換 'COM3' 為你的串列埠，9600 是波特率
with serial.Serial(portName, 19200, timeout=1) as ser:
    # 1 是裝置地址，替換為你的 Modbus 裝置地址
    instrument = minimalmodbus.Instrument(ser.port, 1)

    try:
        # 0 是寄存器地址，3 是功能碼（根據模擬軟體的設定）
        value = instrument.read_register(0, functioncode=3)

        # 處理讀取到的數據
        print(f'Read value: {value}')

    except Exception as e:
        print(f'Error: {e}')

#這是com0com的載點：https://sourceforge.net/projects/com0com/