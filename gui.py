import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QFileDialog,
                             QWidget, QVBoxLayout, QLabel, QScrollArea, QMessageBox)
from PyQt6.QtCore import QSize, Qt
from import_tags import readTagList, importTags
from sql2csv import sql2csv

class ImportTagsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Tags")
        self.setFixedSize(QSize(400, 400))
        self.filePath = None

        # 0 - get file
        self.b_fileDlg = QPushButton("Choose File...")
        self.b_fileDlg.clicked.connect(self.openFileDlg)

        # 1 - show output
        self.l_list = QLabel("Tags Here...")
        self.l_msg = QLabel("Output Here...")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.l_msg)
        self.vbox.addWidget(self.l_list)
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)

        self.sa_outputPanel = QScrollArea()
        self.sa_outputPanel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.sa_outputPanel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sa_outputPanel.setWidgetResizable(True)
        self.sa_outputPanel.setWidget(self.widget)

        # 2 - import
        self.b_import = QPushButton("Import")
        self.b_import.clicked.connect(self.importClicked)

        # window setup
        layout = QVBoxLayout()
        layout.addWidget(self.b_fileDlg)
        layout.addWidget(self.sa_outputPanel)
        layout.addWidget(self.b_import)

        self.setLayout(layout)

    def openFileDlg(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            ".",
            "Text Files(*.txt)",
        )
        
        self.filePath = fname[0]
        tagList = readTagList(self.filePath)
        tags = tagList[0]
        count = tagList[1]

        self.l_list.setText(tags)
        self.l_msg.setText(f"{count} tags found, proceed to import?\n")

    def importClicked(self):
        if (self.filePath is None):
            msg = "No file selected, please check."
            QMessageBox.critical(self, "Error", msg)
        else:
            status = importTags(self.filePath)
            msg = status[1]
            if (status[0] != 1):
                QMessageBox.information(self, "Import Success", msg)
            else:
                QMessageBox.critical(self, "Import Failed", msg)

class S2CWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL 2 CSV Convert")
        self.setFixedSize(QSize(400, 400))
        self.filePath = None

        self.l_fpath = QLabel("No file selected.")

        # 0 - get file
        self.b_fileDlg = QPushButton("Choose File...")
        self.b_fileDlg.clicked.connect(self.openFileDlg)

        # 1 - convert
        self.b_convert = QPushButton("Convert")
        self.b_convert.clicked.connect(self.convertClicked)

        # window setup
        layout = QVBoxLayout()
        layout.addWidget(self.b_fileDlg)
        layout.addWidget(self.l_fpath)
        layout.addWidget(self.b_convert)

        self.setLayout(layout)

    def openFileDlg(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            ".",
            "SQL Files(*.sql)",
        )
        
        self.filePath = fname[0]

        self.l_fpath.setText(f"File selected: {self.filePath}")

    def convertClicked(self):
        if (self.filePath is None):
            msg = "No file selected, please check."
            QMessageBox.critical(self, "Error", msg)
        else:
            msg = sql2csv(self.filePath)
            QMessageBox.information(self, "Convert Success", msg)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TOOLS 4 OPCDA")
        self.setFixedSize(QSize(500, 500))
        self.w = None

        self.b_importTags = QPushButton("Import Tags")
        self.b_importTags.clicked.connect(self.go2ImportTagsWindow)
        self.b_s2c = QPushButton("SQL 2 CSV")
        self.b_s2c.clicked.connect(self.go2s2cWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.b_importTags)
        layout.addWidget(self.b_s2c)

        self.mainLayout = QWidget()
        self.mainLayout.setLayout(layout)

        self.setCentralWidget(self.mainLayout)

    def go2ImportTagsWindow(self):
        if self.w is None:
            self.w = ImportTagsWindow()
            self.w.show()

        else:
            self.w.close()
            self.w = None

    def go2s2cWindow(self):
        if self.w is None:
            self.w = S2CWindow()
            self.w.show()

        else:
            self.w.close()
            self.w = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())