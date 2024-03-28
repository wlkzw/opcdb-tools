import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QFileDialog,
                             QWidget, QVBoxLayout, QLabel, QScrollArea, QMessageBox)
from PyQt6.QtCore import QSize, Qt
from import_tags import readTagList, importTags

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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TOOLS 4 OPCDA")
        self.setFixedSize(QSize(500, 500))
        self.w = None

        self.b_importTags = QPushButton("Import Tags")
        self.b_importTags.clicked.connect(self.go2ImportTagsWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.b_importTags)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())