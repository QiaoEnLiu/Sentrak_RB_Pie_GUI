import minimalmodbus, serial
# 設置串列通訊
ser = serial.Serial('COM3', 19200, timeout=1)  # 替換 'COM3' 為你的串列埠，9600 是波特率

# 設置Modbus裝置
instrument = minimalmodbus.Instrument(ser.port, 1)  # 1 是裝置地址

try:
    # 讀取保持寄存器中的數據（根據你的模擬軟體設定）
    value = instrument.read_register(0, functioncode=3)  # 0 是寄存器地址，3 是功能碼（根據模擬軟體的設定）

    # 處理讀取到的數據
    print(f'Read value: {value}')

except Exception as e:
    print(f'Error: {e}')

finally:
    # 關閉串列通訊
    ser.close()

#這是com0com的載點：https://sourceforge.net/projects/com0com/