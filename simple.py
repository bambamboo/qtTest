from sqlite3.dbapi2 import Error
import time
import random
import pyttsx3
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5 import QtSql
from PyQt5.QtCore import (
    QAbstractProxyModel, QAbstractTableModel, 
    QModelIndex,
    QPersistentModelIndex, QPoint, QSortFilterProxyModel,
    Qt,
    QAbstractItemModel,
    qDebug,
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
    QComboBox, QDialog,
    QHeaderView, 
    QListView,
    QMainWindow,
    QMessageBox, QPushButton,
    QTableView,
    QWidget,
    QAbstractItemView,
    )
import destination2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)
        MainWindow.setMinimumSize(QtCore.QSize(700, 600))
        MainWindow.setMaximumSize(QtCore.QSize(700, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_call = QtWidgets.QPushButton(self.centralwidget)
        self.btn_call.setGeometry(QtCore.QRect(558, 480, 131, 71))
        self.btn_call.setObjectName("btn_call")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_call.setFont(font)
        self.btn_add = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add.setGeometry(QtCore.QRect(10, 480, 89, 71))
        self.btn_add.setStyleSheet("")
        self.btn_add.setObjectName("btn_add")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_add.setFont(font)
        self.btn_delete = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete.setGeometry(QtCore.QRect(120, 480, 89, 71))
        self.btn_delete.setObjectName("btn_delete")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_delete.setFont(font)
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(230, 480, 89, 71))
        self.btn_search.setObjectName("btn_search")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_search.setFont(font)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 434, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(335, 434, 121, 31))
        self.comboBox.setObjectName("comboBox")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox.setFont(font)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 681, 411))
        self.tableView.setObjectName("tableView")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tableView.setFont(font)
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
        #self.actionPlace_windows = QtWidgets.QAction(MainWindow)
        #self.actionPlace_windows.setObjectName("actionPlace_windows")
        self.actionini_py = QtWidgets.QAction(MainWindow)
        self.actionini_py.setObjectName("actionini_py")
        self.actionDestination = QtWidgets.QAction(MainWindow)
        self.actionDestination.setObjectName("actionDestination")
        self.actionDrop_tablel = QtWidgets.QAction(MainWindow)
        self.actionDrop_tablel.setObjectName("actionDrop_tablel")
        self.menuSetting.addAction(self.action_Invite_window)
        #self.menuSetting.addAction(self.actionPlace_windows)
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
        self.btn_call.clicked.connect(self.speak)
        self.btn_search.clicked.connect(self.searchData)
        self.actionDestination.triggered.connect(self.show_desDialog)
        

    def show_desDialog(self):
        self.desDialog.show()

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
        self.action_Invite_window.setText(_translate("MainWindow", "Call sentence setting"))
        #self.actionPlace_windows.setText(_translate("MainWindow", "Place sentence"))
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
        self.tableView.setColumnWidth(1,210)

        # เรียก fetchData เพื่อ fetch data เข้ามาใน model ให้หมด
        self.fetchData()
       
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

        # สร้าง obj ของ destination setting ไว้รอเรียก
        self.desDialog = QtWidgets.QDialog()
        self.ui = destination2.Ui_Dialog()
        self.ui.setupUi(self.desDialog)

    def insertData(self):
        q_number = self.lineEdit.text()
        q_localtime = time.localtime()
        q_enter_time = time.strftime("%H:%M:%S",q_localtime)

        # q_number ต้องไม่ใช่ค่าเว้นวรรค และ ต้องไม่ใช่ค่าว่าง
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

    def searchData(self):
        self.fetchData()
        q_number = self.lineEdit.text()
        totleRow = self.tableView.model().rowCount()
        foundStatus = False

        # q_number ต้องไม่ใช่ค่าเว้นวรรค และ ต้องไม่ใช่ค่าว่าง
        if not q_number.isspace() and q_number != '':
            i = 0
            for i in range(totleRow):

                # เก็บค่า q_number จาก tableView
                s_number = self.tableView.model().data(self.tableView.model().index(i, 1))
                
                # เทียบค่า q_number ของ lineEdit กับ tableView
                if q_number == s_number:
                    print('found this number.')
                    foundStatus = True
                    break
                else:
                    foundStatus = False

            if foundStatus == True:
                self.tableView.selectRow(i)
            else:
                self.showDialog('ค้นหมายเลข ' + q_number + ' ไม่พบ')

        else:
            self.showDialog('กรุณากรอกหมายเลขที่จะค้นก่อน')

    def deleteData(self):
        try:
            # เก็บค่า text จาก column
            current_row = self.tableView.selectedIndexes()
            current_itemUse = current_row[0]
            q_number = self.tableView.model().data(
                self.tableView.model().index(current_itemUse.row(), 1))
        except:
            self.showDialog('กรุณาเลือกหมายเลขที่จะลบก่อน')
            return 

        if q_number == None:
            self.showDialog('เกิดข้อผิดพลาดระหว่างการลบ')
            self.model.select()
            return
        
        # ยืนยันการลบด้วย code 1024
        temp = self.confDelete(q_number)
        if temp == 1024:
            current_item = self.tableView.selectedIndexes()
            for index in current_item:
                self.model.removeRow(index.row())
            self.model.select()
            print('Record deleted.')
            self.showDialog('ลบหมายเลขแล้ว')
        else:
            print('User decided cancel delete this record.')
        
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

    def speak(self):
        try:
            # เก็บค่า text จาก column
            current_row = self.tableView.selectedIndexes()
            current_inUse = current_row[0]
            q_numberText = self.tableView.model().data(
                self.tableView.model().index(current_inUse.row(), 1))
            des_idText = self.tableView.model().data(
                self.tableView.model().index(current_inUse.row(), 5))
        except:
            self.showDialog('กรุณาเลือกหมายเลขที่จะเรียกก่อน')
            return

        # ยืนยันการเรียกด้วย code 1024
        temp = self.confSpeak(q_numberText)
        if temp == 1024:
            engine = pyttsx3.init()
            """ RATE"""
            rate = engine.getProperty('rate')
            #print (rate)
            engine.setProperty('rate', 110)
            """VOLUME"""
            volume = engine.getProperty('volume')
            #print (volume)
            engine.setProperty('volume',1.0)
            """VOICE"""
            voices = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_THAI'
            engine.setProperty('voice',voices)
            engine.say('ขอเชิญหมายเลข' + q_numberText + 'ที่ช่อง' + des_idText)
            print('result = :'+ q_numberText)
            engine.runAndWait()
            engine.stop()
        else:
            print('User decided cancel call.')

    def confSpeak(self,q_numberText):
        # สร้าง dialog เพื่อยืนยันการเรียกและ return code ยืนยันการเรียกด้วย code 1024
        confMsg = QtWidgets.QMessageBox()
        confMsg.setIcon(QtWidgets.QMessageBox.Warning)
        confMsg.setText('ยืนยันที่จะเรียกหมายเลข : ' + q_numberText)
        confMsg.setWindowTitle('แจ้งเตือน')
        confMsg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        reval = confMsg.exec_()
        return(reval)

    def fetchData(self):
        self.model.select()
        # fetch ข้อมูลจากตารางออกมาให้หมด มีผลตอนใช้ search
        while self.model.canFetchMore() == True:
            #self.tableView.scrollToBottom()
            self.model.fetchMore()
        print('rowCoundt = ' + str(self.model.rowCount()))
        self.tableView.scrollToBottom()

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
