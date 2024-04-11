import sys
import random
from collections import deque
import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer

class Viewer(QWidget):
    # store plots and curves
    plots = {}
    curves = {}

    def __init__(self, data):
        super(Viewer, self).__init__()
        self.data = {k: deque(v.items(), maxlen=len(v)) for k, v in data.items()}
        self.win = QMainWindow()
        self.win.setCentralWidget(self)
        self.win.setFixedSize(800, 400)
        self.win.setWindowTitle("Data Viewer")
        self.grid = QGridLayout(self)

        self.win.show()

    def create_plot(self):
        for c, tag in enumerate(self.data.keys()):
            # every 4 plots go to a new row
            r = int(c / 4)

            # set up the plot
            box = QHBoxLayout()
            plt = pg.PlotWidget()
            plt.setTitle(tag)

            # get time and value lists
            time_value = list(self.data[tag])
            time = [tv[0] for tv in time_value]
            value = [tv[1] for tv in time_value]

            # plot time vs value
            curve = plt.plotItem.plot(time, value)

            # add plot and curve to dictionaries
            self.plots[tag] = plt
            self.curves[tag] = {"plot" : curve}

            # add plot to grid
            box.addWidget(plt)
            self.grid.addLayout(box, r, c % 4)

    def update_plot(self):
        for tag in self.data.keys():
            time_value = self.data[tag]
            time = [tv[0] for tv in time_value]
            value = [tv[1] for tv in time_value]

            time.append(time[-1] + 1)
            value.append(random.uniform(0.3, 2.5))
            self.curves[tag]["plot"].setData(time, value)

            self.data[tag].append((time[-1], value[-1]))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        n = 16
        d_td = {}
        
        for x in range(n):
            d_tv = {}
            for i in range(n):
                d_tv[i] = random.uniform(0.3, 2.5)
            d_td[x] = d_tv

        self.viewer = Viewer(d_td)
        self.viewer.create_plot()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.viewer.update_plot)
        self.timer.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    # main.show()
    app.exec()