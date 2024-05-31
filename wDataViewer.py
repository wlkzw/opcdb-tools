import pytz
import pyqtgraph as pg
from collections import deque
from pyqtgraph import DateAxisItem
from PyQt6.QtWidgets import (QMainWindow, QWidget, QGridLayout, 
                             QHBoxLayout, QPushButton, QInputDialog)
from PyQt6.QtCore import QTimer
from datetime import timezone, datetime
from get_data import get_last, get_all
from get_config import get_db_config
from DB_connect import connect_to_mysql

class CustomDateAxisItem(DateAxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value, tz=timezone.utc).strftime('%H:%M:%S') for value in values]

class Viewer(QWidget):
    # store plots and curves
    plots = {}
    curves = {}

    def __init__(self, data):
        super(Viewer, self).__init__()
        self.data = {k: deque(v.items(), maxlen=len(v)) for k, v in data.items()}
        self.win = QMainWindow()
        self.win.setCentralWidget(self)
        # self.win.setFixedSize(800, 400)
        self.win.setWindowTitle("Data Viewer")
        self.grid = QGridLayout(self)
        self.grid.setSpacing(10)

        self.win.show()

    def create_plot(self):
        button_layout = QHBoxLayout()
        self.grid.addLayout(button_layout, 0, 0, 1, 4)

        for c, tag in enumerate(self.data.keys()):
            # every 4 plots go to a new row
            r = int(c / 4) + 1

            button = QPushButton(f"Set range for {tag}")
            button.clicked.connect(lambda checked, t=tag: self.set_range(t))
            button_layout.addWidget(button)

            # set up the plot
            box = QHBoxLayout()
            date_axis = CustomDateAxisItem(orientation='bottom')
            plt = pg.PlotWidget(axisItems={'bottom': date_axis})
            plt.setTitle(tag)
            plt.showGrid(x=True, y=True)

            # get time and value lists
            time_value = list(self.data[tag])
            time = [tv[0].replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Shanghai')).timestamp() for tv in time_value]
            value = [float(tv[1]) for tv in time_value]

            print(f"initial time:  {time}\ninitial value: {value}")

            # plot time vs value
            curve = plt.plotItem.plot(time, value)

            # add plot and curve to dictionaries
            self.plots[tag] = plt
            self.curves[tag] = {"plot" : curve}

            # add plot to grid
            box.addWidget(plt)
            self.grid.addLayout(box, r, c % 4)

    def update_plot(self):
        cnx = connect_to_mysql(get_db_config("db_config.xml"))
        for tag in self.data.keys():
            time_value = self.data[tag]

            print(f"-----\nold: {time_value}\n------")

            time = deque([tv[0].replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Shanghai')).timestamp() for tv in time_value], maxlen=len(time_value))
            value = deque([float(tv[1]) for tv in time_value], maxlen=len(time_value))

            print(f"old time:  {time}\nold value: {value}")

            new_tv = get_last(cnx, [tag])
            new_time = new_tv[0][2].replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Shanghai')).timestamp()
            new_value = float(new_tv[0][1])

            print(f"get time:  {new_time}\nget value: {new_value}")

            time.appendleft(new_time)
            value.appendleft(new_value)

            print(f"new time:  {time}\nnew value: {value}")

            self.curves[tag]["plot"].setData(time, value)

            self.data[tag].appendleft((datetime.fromtimestamp(time[0], pytz.UTC), value[0]))

            print(f"-----\nnew: {self.data[tag]}\n-----")

    def set_range(self, tag):
        # get the current y values
        y_values = [float(tv[1]) for tv in self.data[tag]]

        # calculate the current range
        y_min = min(y_values)
        y_max = max(y_values)

        # ask the user for the new range
        new_y_min, ok = QInputDialog.getDouble(self, "Set y-axis range", "Enter y min:", y_min)
        if ok:
            new_y_max, ok = QInputDialog.getDouble(self, "Set y-axis range", "Enter y max:", y_max)
            if ok:
                # set the y range of the plot
                self.plots[tag].setYRange(new_y_min, new_y_max)

class DataViewer(QWidget):
    def __init__(self, l_tags, parent=None):
        super(DataViewer, self).__init__(parent)

        config = get_db_config("db_config.xml")
        cnx = connect_to_mysql(config)

        n = len(l_tags)
        d_data = {}
        
        for i in range(n):
            d_tv = {}
            l_data = get_all(cnx, [l_tags[i]])
            count = 0
            for j in reversed(l_data):
                if count < 5:
                    time = j[-1]
                    value = j[1]
                    d_tv[time] = value
                    count += 1
                else:
                    break
            d_data[l_tags[i]] = d_tv

        self.viewer = Viewer(d_data)
        self.viewer.create_plot()

        self.timer = QTimer()
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.viewer.update_plot)
        self.timer.start()