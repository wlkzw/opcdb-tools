import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Value", "Function"])

        self.addButton = QPushButton("Add Row")
        self.addButton.clicked.connect(self.addRow)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.addButton)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("storage")
        self.db.setUserName("root")
        self.db.setPassword("123456")
        ok = self.db.open()
        if ok:
            print("Connected to MySQL")
            self.populateTable()  # Fetch data from the database and populate the table
        else:
            print("Connection failed")

    def populateTable(self):
        query = QSqlQuery("SELECT `name`, `function`, `value` FROM data")
        while query.next():
            name = query.value(0)
            function = query.value(1)
            value = query.value(2)

            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)

            self.table.setItem(rowPosition, 0, QTableWidgetItem(name))
            self.table.setItem(rowPosition, 1, QTableWidgetItem(value))
            self.table.setItem(rowPosition, 2, QTableWidgetItem(function))


    def addRow(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)

        name, okPressed = QInputDialog.getText(self, "Get text","Name:")
        if okPressed and name != '':
            self.table.setItem(rowPosition, 0, QTableWidgetItem(name))

        function, okPressed = QInputDialog.getText(self, "Get text","Function:")
        if okPressed and function != '':
            self.table.setItem(rowPosition, 2, QTableWidgetItem(function))

            # Check if function is a function of existing data
            try:
                value = eval(function, {name: self.table.item(rowPosition, 1).text() for name in range(rowPosition)})
                self.table.setItem(rowPosition, 1, QTableWidgetItem(str(value)))
            except:
                pass

        # Update the MySQL database
        query = QSqlQuery()
        query.prepare("INSERT INTO data (`name`, `function`, `value`) VALUES (?, ?, ?)")
        query.addBindValue(name)
        query.addBindValue(function)
        query.addBindValue(str(value))
        
        if not query.exec():
            print("Query failed:", query.lastError().text())
        else:
            print("Query executed successfully")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec())