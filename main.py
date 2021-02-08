import sys

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
)

#ติดต่อฐานข้อมูล#
class createConnection():

    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("ex1")
    con.open()
    print('After OPEN command isOpen : ' + str(con.isOpen()))
    query = QSqlQuery()
    query.exec('SELECT * FROM queue')
    query.finish()
    con.close()
    con.removeDatabase("ex1")


class Contacts(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTableView Example")
        self.resize(800, 600)
        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable("queue")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "q_id")
        self.model.setHeaderData(1, Qt.Horizontal, "q_name")
        self.model.setHeaderData(2, Qt.Horizontal, "q_time_enter")
        self.model.setHeaderData(3, Qt.Horizontal, "q_time_call")
        self.model.setHeaderData(4, Qt.Horizontal, "q_status")
        self.model.setHeaderData(5, Qt.Horizontal, "q_destination")

        self.model.select()
        # Set up the view
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)

app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = Contacts()
win.show()
sys.exit(app.exec_())
