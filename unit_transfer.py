
class unit_transfer():
    def set_temperature_unit(unit):
        """設定溫度單位"""
        # print('溫度單位:', unit)
        if unit.lower() in ['celsius', '華氏']:  # 將使用者輸入轉為小寫比對
            unit = '°C'
        elif unit.lower() in ['fahrenheit', '攝氏']:  # 將使用者輸入轉為小寫比對
            unit = '°F'
        else:
            print("請輸入有效的溫度單位（攝氏或華氏）")
        return unit

    def convert_temperature(temperature, unit):
        """根據溫度單位轉換溫度"""
        if unit.lower() == 'fahrenheit':
            return (temperature - 32) * 5/9  # 華氏轉攝氏
        elif unit.lower() == 'celsius':
            return (temperature * 9/5) + 32  # 攝氏轉華氏
        else:
            print("請輸入有效的溫度單位（攝氏或華氏）")