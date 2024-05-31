from PyQt6.QtWidgets import (QPushButton, QFileDialog, QInputDialog,
                             QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QLabel)
from PyQt6.QtGui import QColor

from data_preparation import FileToList, Insert_formulaToDB
from update_calculation import update_calculation

class CalcWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("软仪表")
        self.setGeometry(300,300,600, 600)  # Adjusted window size
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        label = QLabel("状态显示")
        label.setStyleSheet("font-size: 20px;")
        main_layout.addWidget(label)
        self.message_box = QTextEdit()
        self.message_box.setStyleSheet("background-color: white; "
                                       "color: black; "
                                       "font-size: 14px;")
        self.message_box.setReadOnly(True)  # Make the text edit read-only  # Set fixed height for the text box
        self.print_message("Welcome!")
        main_layout.addWidget(self.message_box)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        button_read_file = QPushButton("Choose File")
        button_read_file.clicked.connect(self.open_file)
        button_read_file.setFixedHeight(40)  # Set larger button height
        button_read_file.setStyleSheet("font-size: 13px;")  # Increase font size

        start_calculation = QPushButton("Start Calculation")
        start_calculation.clicked.connect(self.start_calculation)
        start_calculation.setFixedHeight(40)  # Set larger button height
        start_calculation.setStyleSheet("font-size: 13px;")  # Increase font size

        end_calculation = QPushButton("End Calculation")
        end_calculation.clicked.connect(self.end_calculation)
        end_calculation.setFixedHeight(40)  # Set larger button height
        end_calculation.setStyleSheet("font-size: 13px;")  # Increase font size
        
        button_layout.addWidget(button_read_file)
        button_layout.addWidget(start_calculation)
        button_layout.addWidget(end_calculation)

        self.calculation = update_calculation(self)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 
                                                   "Open File", 
                                                   "", 
                                                   "Text Files (*.txt)")
        if file_path:
            function = FileToList(file_path)
            Insert_formulaToDB(function)
            self.print_message("File loaded successfully.")
        else:
            self.print_message("<font color = 'red'>File loaded fail.")

    def start_calculation(self):
        period, okPressed = QInputDialog.getText(self, "Frequency of Calculation", "Enter Frequency:")
        if okPressed and period.isdigit() and int(period) > 0:
            self.print_message(f"Calculation started with frequency: {period}")
            self.calculation.trigger_timer(int(period))

    def end_calculation(self):
        self.calculation.stop_timer()

    def print_message(self, message):
        self.message_box.append(message)
