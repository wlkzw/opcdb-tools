import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton,QWidget, QVBoxLayout)
from PyQt6.QtCore import QSize, QThread
from wImportTags import ImportTagsWindow
from wS2C import S2CWindow
from wCalculation import CalcWindow
from wSelectTags import TagSelectionWindow

__version__ = "1.0.0"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(f"TOOLS 4 OPCDA - v{__version__}")
        self.setFixedSize(QSize(500, 500))
        self.windows = {}
        self.threads = {}

        self.qb_importTags = QPushButton("Import Tags")
        self.qb_importTags.setMinimumHeight(30)
        self.qb_importTags.clicked.connect(self.go2ImportTagsWindow)
        self.qb_calc = QPushButton("Calculation")
        self.qb_calc.setMinimumHeight(30)
        self.qb_calc.clicked.connect(self.go2CalcWindow)
        self.qb_trends = QPushButton("Live Trends")
        self.qb_trends.setMinimumHeight(30)
        self.qb_trends.clicked.connect(self.go2TrendsWindow)
        self.qb_s2c = QPushButton("SQL 2 CSV")
        self.qb_s2c.setMinimumHeight(30)
        self.qb_s2c.clicked.connect(self.go2s2cWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.qb_importTags)
        layout.addWidget(self.qb_calc)
        layout.addWidget(self.qb_trends)
        layout.addWidget(self.qb_s2c)

        self.mainLayout = QWidget()
        self.mainLayout.setLayout(layout)

        self.setCentralWidget(self.mainLayout)

    def go2ImportTagsWindow(self):
        if "ImportTagsWindow" not in self.windows:
            self.windows["ImportTagsWindow"] = ImportTagsWindow()
            self.threads["ImportTagsWindow"] = QThread()
            self.windows["ImportTagsWindow"].moveToThread(self.threads["ImportTagsWindow"])
            self.threads["ImportTagsWindow"].started.connect(self.windows["ImportTagsWindow"].show)
            self.threads["ImportTagsWindow"].start()
        else:
            self.windows["ImportTagsWindow"].close()
            del self.windows["ImportTagsWindow"]

    def go2CalcWindow(self):
        if "CalcWindow" not in self.windows:
            self.windows["CalcWindow"] = CalcWindow()
            self.threads["CalcWindow"] = QThread()
            self.windows["CalcWindow"].moveToThread(self.threads["CalcWindow"])
            self.threads["CalcWindow"].started.connect(self.windows["CalcWindow"].show)
            self.threads["CalcWindow"].start()
        else:
            self.windows["CalcWindow"].close()
            del self.windows["CalcWindow"]

    def go2TrendsWindow(self):
        if "TagSelectionWindow" not in self.windows:
            self.windows["TagSelectionWindow"] = TagSelectionWindow()
            self.threads["TagSelectionWindow"] = QThread()
            self.windows["TagSelectionWindow"].moveToThread(self.threads["TagSelectionWindow"])
            self.threads["TagSelectionWindow"].started.connect(self.windows["TagSelectionWindow"].show)
            self.threads["TagSelectionWindow"].start()
        else:
            self.windows["TagSelectionWindow"].close()
            del self.windows["TagSelectionWindow"]

    def go2s2cWindow(self):
        if "s2cWindow" not in self.windows:
            self.windows["s2cWindow"] = S2CWindow()
            self.threads["s2cWindow"] = QThread()
            self.windows["s2cWindow"].moveToThread(self.threads["s2cWindow"])
            self.threads["s2cWindow"].started.connect(self.windows["s2cWindow"].show)
            self.threads["s2cWindow"].start()
        else:
            self.windows["s2cWindow"].close()
            del self.windows["s2cWindow"]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())