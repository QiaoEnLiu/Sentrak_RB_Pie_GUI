#zh-tw
# PlotCanvas.py
#初始子畫面折線圖


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# matplotlib.use('Qt5Agg')

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