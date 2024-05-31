from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QListWidget, QPushButton, QAbstractItemView)
from PyQt6.QtCore import QSize
from wDataViewer import DataViewer
from get_data import get_all_tag
from get_config import get_db_config
from DB_connect import connect_to_mysql

class TagSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Tags")
        self.setFixedSize(QSize(400, 400))

        config = get_db_config("db_config.xml")
        self.cnx = connect_to_mysql(config)

        self.list_widget = QListWidget()
        self.list_widget.addItems(get_all_tag(self.cnx))
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.button = QPushButton("See live trends")
        self.button.clicked.connect(self.plot_selected_curves)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def plot_selected_curves(self):
        # get the selected items
        selected_items = self.list_widget.selectedItems()
        selected_tags = [item.text() for item in selected_items]

        # create a DataViewer and pass the selected tags
        self.viewer = DataViewer(selected_tags, self)
        self.viewer.show()
    