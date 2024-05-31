from PyQt6.QtWidgets import (QPushButton, QFileDialog, QWidget, QVBoxLayout, 
                             QLabel, QMessageBox, QProgressBar)
from PyQt6.QtCore import QSize
from sql2csv import sql2csv

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