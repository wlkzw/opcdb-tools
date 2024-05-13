import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QFileDialog,
                             QWidget, QVBoxLayout, QLabel, QScrollArea, QMessageBox,
                             QProgressBar)
from PyQt6.QtCore import QSize, Qt
from import_tags import import_tags, read_tags
from sql2csv import sql2csv

__version__ = "1.0.0"

class ImportTagsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Tags")
        self.setFixedSize(QSize(400, 400))
        self.filePath = None

        # 0 - get file
        self.qb_fileDlg = QPushButton("Choose File...")
        self.qb_fileDlg.clicked.connect(self.openFileDlg)

        # 1 - show output
        self.ql_list = QLabel("Tags Here...")
        self.ql_msg = QLabel("Output Here...")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.ql_msg)
        self.vbox.addWidget(self.ql_list)
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)

        self.qsa_outputPanel = QScrollArea()
        self.qsa_outputPanel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.qsa_outputPanel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.qsa_outputPanel.setWidgetResizable(True)
        self.qsa_outputPanel.setWidget(self.widget)

        # 2 - import
        self.qb_import = QPushButton("Import")
        self.qb_import.clicked.connect(self.importClicked)

        # window setup
        layout = QVBoxLayout()
        layout.addWidget(self.qb_fileDlg)
        layout.addWidget(self.qsa_outputPanel)
        layout.addWidget(self.qb_import)

        self.setLayout(layout)

    def openFileDlg(self):
        try:
            fname = QFileDialog.getOpenFileName(
                self,
                "Open File",
                ".",
                "Text Files(*.txt)",
            )
            
            self.filePath = fname[0]
            l_tags = read_tags(self.filePath)
            print_tags = "\n".join(l_tags)
            count = len(l_tags)

            self.ql_list.setText(print_tags)
            self.ql_msg.setText(f"{count} tags found, proceed to import?\n")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def importClicked(self):
        try:
            if (self.filePath is None):
                msg = "No file selected, please check."
                QMessageBox.critical(self, "Error", msg)
            else:
                status = import_tags(self.filePath)
                msg = status[1]
                if (status[0] != 1):
                    QMessageBox.information(self, "Import Success", msg)
                else:
                    QMessageBox.critical(self, "Import Failed", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class S2CWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL 2 CSV Convert")
        self.setFixedSize(QSize(400, 400))
        self.filePath = None

        self.ql_message = QLabel("No file selected.")
        self.ql_message.setWordWrap(True)
        self.pbar = QProgressBar(self)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(100)

        # 0 - get file
        self.qb_fileDlg = QPushButton("Choose File...")
        self.qb_fileDlg.clicked.connect(self.openFileDlg)

        # 1 - convert
        self.qb_convert = QPushButton("Convert")
        self.qb_convert.clicked.connect(self.convertClicked)

        # window setup
        layout = QVBoxLayout()
        layout.addWidget(self.qb_fileDlg)
        layout.addWidget(self.ql_message)
        layout.addWidget(self.pbar)
        layout.addWidget(self.qb_convert)

        self.setLayout(layout)

    def openFileDlg(self):
        try:
            fname = QFileDialog.getOpenFileName(
                self,
                "Open File",
                ".",
                "SQL Files(*.sql)",
            )   
            
            self.filePath = fname[0]
            self.ql_message.setText(f"File selected: {self.filePath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def convertClicked(self):
        try:
            if (self.filePath is None):
                msg = "No file selected, please check."
                QMessageBox.critical(self, "Error", msg)
            else:
                sql2csv(self.filePath, self.pbar, self.ql_message)
                QMessageBox.information(self, "Success", "Conversion completed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(f"TOOLS 4 OPCDA - v{__version__}")
        self.setFixedSize(QSize(500, 500))
        self.qmw = None

        self.qb_importTags = QPushButton("Import Tags")
        self.qb_importTags.clicked.connect(self.go2ImportTagsWindow)
        self.qb_s2c = QPushButton("SQL 2 CSV")
        self.qb_s2c.clicked.connect(self.go2s2cWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.qb_importTags)
        layout.addWidget(self.qb_s2c)

        self.mainLayout = QWidget()
        self.mainLayout.setLayout(layout)

        self.setCentralWidget(self.mainLayout)

    def go2ImportTagsWindow(self):
        if self.qmw is None:
            self.qmw = ImportTagsWindow()
            self.qmw.show()

        else:
            self.qmw.close()
            self.qmw = None

    def go2s2cWindow(self):
        if self.qmw is None:
            self.qmw = S2CWindow()
            self.qmw.show()

        else:
            self.qmw.close()
            self.qmw = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())