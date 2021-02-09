import sys

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from PyQt5.QtWidgets import (
    QAbstractItemView, QApplication, QComboBox, QHeaderView,
    QMainWindow,
    QMessageBox,
    QTableView,
)

class Contacts(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTableView Example")
        self.resize(800, 600)

        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable("queue")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Number")
        self.model.setHeaderData(2, Qt.Horizontal, "Enter Time")
        self.model.setHeaderData(3, Qt.Horizontal, "Call Time")
        self.model.setHeaderData(4, Qt.Horizontal, "Status")       
        self.model.setHeaderData(5, Qt.Horizontal, "Destination")
        self.model.select()

        # Set up the view
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setColumnHidden(0,True)
        self.view.setCornerButtonEnabled(False)
        #self.view.setEditTriggers(QAbstractItemView())
        #self.headerView = QHeaderView()
        #self.view.setHorizontalHeader()
        #print(str(self.view.editTriggers()))       
        self.view.resizeColumnsToContents()

        i = self.view.model().index(1,5)

        # self.cbxModel = QSqlQueryModel(self)
        # self.cbxModel.setQuery = "SELECT des_name FROM destination"
        # self.cbxModel.query()
        self.cbxModel = QSqlTableModel(self)
        self.cbxModel.setTable("destination")
        self.cbxModel.select()

        self.cbxView = QComboBox()
        self.cbxView.setModel(self.cbxModel)
        # เลือก column ที่จะมาแสดง
        self.cbxView.setModelColumn(1)
        
        self.view.setIndexWidget(i,self.cbxView)
        self.setCentralWidget(self.view)


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("ex1")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = Contacts()
win.show()
sys.exit(app.exec_())
