from sqlite3.dbapi2 import Error
import time
import random
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5 import QtSql
from PyQt5.QtCore import (
    QAbstractTableModel, 
    QModelIndex,
    QPersistentModelIndex, QPoint,
    Qt,
    QAbstractItemModel, qDebug
    )
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlQueryModel, QSqlRecord,
    QSqlRelation,
    QSqlRelationalDelegate,
    QSqlRelationalTableModel,
    QSqlTableModel,
    )
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QHeaderView, 
    QListView,
    QMainWindow,
    QMessageBox, QPushButton,
    QTableView,
    QWidget,
    QAbstractItemView,
    )

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)
        MainWindow.setMinimumSize(QtCore.QSize(700, 500))
        MainWindow.setMaximumSize(QtCore.QSize(700, 500))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_call = QtWidgets.QPushButton(self.centralwidget)
        self.btn_call.setGeometry(QtCore.QRect(558, 380, 131, 71))
        self.btn_call.setObjectName("btn_call")
        self.btn_add = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add.setGeometry(QtCore.QRect(10, 380, 89, 71))
        self.btn_add.setStyleSheet("")
        self.btn_add.setObjectName("btn_add")
        self.btn_delete = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete.setGeometry(QtCore.QRect(120, 380, 89, 71))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(230, 380, 89, 71))
        self.btn_search.setObjectName("btn_search")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 334, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(335, 334, 121, 31))
        self.comboBox.setObjectName("comboBox")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 681, 311))
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menubar.setObjectName("menubar")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Invite_window = QtWidgets.QAction(MainWindow)
        self.action_Invite_window.setObjectName("action_Invite_window")
        self.actionPlace_windows = QtWidgets.QAction(MainWindow)
        self.actionPlace_windows.setObjectName("actionPlace_windows")
        self.actionini_py = QtWidgets.QAction(MainWindow)
        self.actionini_py.setObjectName("actionini_py")
        self.actionDestination = QtWidgets.QAction(MainWindow)
        self.actionDestination.setObjectName("actionDestination")
        self.actionDrop_tablel = QtWidgets.QAction(MainWindow)
        self.actionDrop_tablel.setObjectName("actionDrop_tablel")
        self.menuSetting.addAction(self.action_Invite_window)
        self.menuSetting.addAction(self.actionPlace_windows)
        self.menuSetting.addAction(self.actionDestination)
        self.menuSetting.addAction(self.actionDrop_tablel)
        self.menuSetting.addSeparator()
        self.menuSetting.addAction(self.actionini_py)
        self.menubar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # เรียกฟังชั่นเพื่อโหลด model ลง table
        self.loadData()

        self.btn_add.clicked.connect(self.insertData)
        self.btn_delete.clicked.connect(self.deleteData)
        self.btn_call.clicked.connect(self.insertDev)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simple Queue"))
        self.btn_call.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อเรียกคิวที่เลือกจากตารางคิว</p></body></html>"))
        self.btn_call.setText(_translate("MainWindow", "CALL"))
        self.btn_add.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อเปิดเมนูการเพิ่มคิวด้วยตัวเอง</p></body></html>"))
        self.btn_add.setText(_translate("MainWindow", "M-ADD"))
        self.btn_delete.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อลบคิวที่ป้อนค่าผิดออกจากตารางคิว</p></body></html>"))
        self.btn_delete.setText(_translate("MainWindow", "DELETE"))
        self.btn_search.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อโหลดตารางคิวใหม่</p></body></html>"))
        self.btn_search.setText(_translate("MainWindow", "SEARCH"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.action_Invite_window.setText(_translate("MainWindow", "Invite sentence"))
        self.actionPlace_windows.setText(_translate("MainWindow", "Place sentence"))
        self.actionini_py.setText(_translate("MainWindow", "ini.py"))
        self.actionDestination.setText(_translate("MainWindow", "Destination setting"))
        self.actionDrop_tablel.setText(_translate("MainWindow", "Drop tablel"))

    def loadData(self):
        self.lineEdit.clear()
        self.lineEdit.setFocus()
        # สร้าง model เรียก data จาก database
        # ใช้ QSqlRelationalTableModel สำหรับตารางที่มีคีย์นอก
        self.model = QSqlRelationalTableModel()
        self.model.setTable('queue')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, 'ID')
        self.model.setHeaderData(1, Qt.Horizontal, "Number")
        self.model.setHeaderData(2, Qt.Horizontal, "Enter Time")
        self.model.setHeaderData(3, Qt.Horizontal, "Call Time")
        self.model.setHeaderData(4, Qt.Horizontal, "Status")
        self.model.setHeaderData(5, Qt.Horizontal, "Destination")
        self.model.setHeaderData(6, Qt.Horizontal, "Option")

        # ให้ column#5 เป็นคีย์นอกดึงตารางนอกมาแสดง
        self.model.setRelation(5, QSqlRelation(
            "destination", "des_id", "des_name"))  

        # เรียกใช้ model เรียกใช้ได้จากทุกที่ใน class ไม่ต้องเรียก loadData()
        self.model.select()

        # ให้ tableView เลือก data จาก model ไปแสดง
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegate(QSqlRelationalDelegate(self.tableView))
        self.tableView.setColumnHidden(0, True)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setSortingEnabled(True)
        self.tableView.resizeColumnsToContents()
        #self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.columnCountChanged(6,7)

        # เมื่อ click ให้เลือกทั้งแถว
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)    

        # สร้าง model เรียกตาราง destination แล้วยัดเข้า combobox
        self.desModel = QSqlQueryModel()
        selectQuery = QSqlQuery()
        selectQuery.prepare('SELECT des_name FROM destination')
        print('QUERY = ' + str(selectQuery.lastQuery()))
        if selectQuery.exec():
            self.desModel.setQuery(selectQuery)      
            print('SELECT des_name COMPLETE')
            self.comboBox.setModel(self.desModel)
        else:
            print('SELECT FALSE = ' + selectQuery.lastError().text())

        # พยายามยัด button เข้า tableView ได้แล้ว แต่ต้องหาวิธีเพิ่ม column combobox ใน tableView
        # for i in range(self.model.rowCount()):
        #     self.btn_test = QPushButton('Del')
        #     index = self.tableView.model().index(i, 5)
        #     self.tableView.setIndexWidget(index, self.btn_test)

        # เก็บค่า text จาก column

    def insertData(self):
        q_number = self.lineEdit.text()
        q_localtime = time.localtime()
        q_enter_time = time.strftime("%H:%M:%S",q_localtime)

        # q_number ต้องไม่ใช่ค่าเว้นวรรค และ ไต้องม่ใช่ค่าว่าง
        if not q_number.isspace() and q_number != '':

            # เรียก getDestination_id เพื่อหาค่า des_id เพื่อใช้ในคำสั่ง sql INSERT
            des_id = self.getDestination_id()
            try:
                insertQuery = QSqlQuery()
                insertQuery.prepare("INSERT INTO queue " + "(q_number,q_enter_time,des_id) " +
                                    "VALUES " + f"('{q_number}','{q_enter_time}',{des_id})")

                print('Query = ' + insertQuery.lastQuery())
                if insertQuery.exec():
                    print('INSERT COMPLETE')
                    self.loadData()
                else:
                    print('INSERT FALSE = ' + insertQuery.lastError().text())
            except(Error) as e:
                print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                      'ERROR :' + str(e))
        else:
            self.showDialog('กรุณากรอกหมายเลขที่จะเพิ่มก่อน')

    def getDestination_id(self):
        # สร้างมาเพื่อให้ return ค่า des_id ในตาราง destination กลับไป
        temp = self.comboBox.currentText()
        desModel = QSqlQueryModel()
        selectQuery = QSqlQuery()
        selectQuery.prepare('SELECT des_id,des_name From destination')
        if selectQuery.exec():
            desModel.setQuery(selectQuery)
            for i in range(desModel.rowCount()):
                if temp == desModel.index(i, 1).data():
                    return desModel.index(i, 0).data()
                else:
                    pass
        else:
            print('SELECT FALSE = ' + selectQuery.lastError().text())
    
    def insertDev(self):
        j = 10
        for i in range(50):
            q_number = random.randint(0,100000)
            q_enter_time = f'18:{j}:00'
            des_id = 4
            #print(q_number)
            insertQuery = QSqlQuery()
            insertQuery.prepare("INSERT INTO queue " + "(q_number,q_enter_time,des_id) " +
                                "VALUES " + f"('{q_number}','{q_enter_time}',{des_id})")
            insertQuery.exec()
            self.model.select()
            j += 1
        print('insertDEV complete')

    def deleteData(self):
        try:
            # เก็บค่า text จาก column
            current_row = self.tableView.selectedIndexes()
            current_itemUse = current_row[0]
            q_number = self.tableView.model().data(
                self.tableView.model().index(current_itemUse.row(), 1))
        except:
            self.showDialog('กรุณาเลือกหมายเลขที่จะลบก่อน')

        try:
            # ยืนยนการลบด้วย code 1024
            if self.confDelete(q_number) == 1024:
                current_item = self.tableView.selectedIndexes()
                for index in current_item:
                    self.model.removeRow(index.row())
                self.model.select()
                print('Record deleted.')
                self.showDialog('ลบหมายเลขแล้ว')
            else:
                print('User decided cancel delete this record.')
        except(Error) as e:
            print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                  'ERROR :' + str(e))

    def confDelete(self,q_number):
        # สร้าง dialog เพื่อยืนยันการลบ และ return code ยืนยันการลบด้วย code 1024
        confMsg = QtWidgets.QMessageBox()
        confMsg.setIcon(QtWidgets.QMessageBox.Critical)
        confMsg.setText('ยืนยันที่จะลบหมายเลข : ' + q_number)
        confMsg.setWindowTitle('แจ้งเตือนการลบ')
        confMsg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        reval = confMsg.exec_()
        return(reval)
        
    def btn_delClicked(self):
        button =QtGui.QGuiApplication.focusObject()
        index = self.tableView.indexAt(button.pos())
        if index.isValid():
            print(index.row(),index.column())

    def showDialog(self,message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('แจ้งเตือน')
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(
            #message + str(time.strftime(" @ %H:%M:%S ", time.localtime())))
            message)
        msg.exec_()

def createConnection():
    # ติดต่อ database ผ่าน driver SQLLITE
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("simple.sqlite")
    if not con.open():
        QMessageBox.critical(
            None,
            "Simple Queue - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True

if __name__ == "__main__":
    import sys

    # เรียกฟังชั่น เพื่อทดสอบติดต่อ database 
    if not createConnection():      
        # หากฟังชั่น return False ให้ system exit
        sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
