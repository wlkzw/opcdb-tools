from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QWidget, 
                             QListWidget, QPushButton, QAbstractItemView)
from PyQt6.QtGui import QColor
import pyqtgraph as pg
import pandas as pd
import sys

class MainWindow(QMainWindow):
    def __init__(self, csv_file):
        super().__init__()

        self.setWindowTitle("Tag Graph")

        # Create a QVBoxLayout instance
        self.layout = QVBoxLayout()

        # Load data from CSV file
        df = pd.read_csv(csv_file)
        df.rename(columns={df.columns[0]: 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        self.df = df

        # Create a QListWidget instance
        self.list_widget = QListWidget()
        self.list_widget.addItems(df.columns[1:])
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        # Create a QPushButton instance
        self.button = QPushButton("Plot selected curves")
        self.button.clicked.connect(self.plot_selected_curves)

        # Add the QListWidget and QPushButton to the layout
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.button)

        # Create a central widget and set the layout
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)

        # Set the central widget
        self.setCentralWidget(self.centralWidget)

        # Initialize the plot_window instance variable
        self.plot_window = None

    def plot_selected_curves(self):
        # Get the selected items
        selected_items = self.list_widget.selectedItems()

        # Create a new QMainWindow instance for the plot
        self.plot_window = QMainWindow()

        # Create a QVBoxLayout instance for the plot_window
        plot_layout = QVBoxLayout()

        # Create a PlotWidget instance with a DateAxisItem
        date_axis = pg.DateAxisItem()
        plot = pg.PlotWidget(axisItems={'bottom': date_axis})

        # Set the plot background to white
        plot.setBackground('w')

        # Add a legend to the plot
        plot.addLegend()

        # Define a color cycle
        colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black']

        # Add a curve for each selected item
        for i, item in enumerate(selected_items):
            column = item.text()
            curve = pg.PlotCurveItem(self.df.index.values.astype('int64')/10**9, self.df[column].values, 
                                     pen=pg.mkPen(color=QColor(colors[i % len(colors)])), name=column)
            plot.addItem(curve)

        # Add the plot to the plot_layout
        plot_layout.addWidget(plot)

        # Create a central widget for the plot_window and set the plot_layout
        plot_centralWidget = QWidget()
        plot_centralWidget.setLayout(plot_layout)

        # Set the central widget of the plot_window
        self.plot_window.setCentralWidget(plot_centralWidget)

        # Show the plot_window
        self.plot_window.show()

if __name__ == "__main__":
    csv_file = "data.csv"

    app = QApplication(sys.argv)

    window = MainWindow(csv_file)
    window.show()

    sys.exit(app.exec())