from PyQt6.QtWidgets import (QPushButton, QFileDialog, QWidget, QVBoxLayout, 
                             QLabel, QScrollArea, QMessageBox)
from PyQt6.QtCore import QSize, Qt
from import_tags import import_tags, read_tags

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
