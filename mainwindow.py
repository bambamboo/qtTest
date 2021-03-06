from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget,QDesktopWidget,QApplication
import time
import sqlite3
from sqlite3 import Error

class Ui_MainWindow(object):

    def loadData(self):
        conn = sqlite3.Connection('ex1')
        query = 'SELECT * FROM queue ORDER BY q_enter_time ASC;'
        try:
            result = conn.execute(query)
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                  'Load data from database success.')
        except(Error) as e:
            print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                  'ERROR :' + str(e))
        conn.close()
        self.lineEdit.setText('')
        self.tableWidget.selectRow(self.tableWidget.rowCount() - 1)
        #self.paintTable()

    def writeData(self):
        conn = sqlite3.Connection('ex1')
        q_number = self.lineEdit.text()
        named_tuple = time.localtime()  # get struct_time
        q_enter_time = time.strftime("%H:%M:%S", named_tuple)
        if q_number != '':
            temp = self.cfDuplicate(q_number)
            if temp == False:
                try:
                    query = 'INSERT INTO queue(q_number,q_enter_time) VALUES(?,?)'
                    cursor = conn.cursor()
                    cursor.execute(query, [q_number, q_enter_time])
                    conn.commit()
                    print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                        'Data saved to database success.')
                    self.openDialog('บันทึกข้อมูลเแล้ว')
                except(Error) as e:
                    print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                        'ERROR :' + str(e))
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Question)
                msg.setText("หมายเลข : " + q_number + " ถูกเพิ่มในตารางแล้ว ต้องการจะเรียกเลยหรือไม่")
                msg.setWindowTitle("แจ้งเตือน")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok |
                                       QtWidgets.QMessageBox.Cancel)
                retval = msg.exec_()
        else:
            print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                  'Got Null value on LineEdit ,Unable to write Null in database.')
            self.openDialog('ไม่สามารถบันทึกหมายเลขว่างได้')
        conn.close()
        self.loadData()

    def cfDuplicate(self, q_number):
        totleRow = self.tableWidget.rowCount()
        foundStatus = False
        for i in range(totleRow):
            if self.tableWidget.item(i, 1).text() == q_number:
                foundStatus = True
                break
            else:
                foundStatus = False  
        return(foundStatus)

    def deleteData(self):
        conn = sqlite3.Connection('ex1')
        cPosition = 1
        rPosition = (int(self.tableWidget.currentRow()))
        if rPosition >= 0:
            q_number = self.tableWidget.item(rPosition, cPosition).text()
            try:
                cfCode = self.cfDelete(q_number)
                if cfCode == 1024:
                    query = 'DELETE FROM queue where q_number = ?'
                    cursor = conn.cursor()
                    cursor.execute(query, [q_number])
                    conn.commit()
                    print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                        'Delete data from database success.')
                    self.openDialog('ลบหมายเลขเแล้ว')
                else:
                    pass
            except(Error) as e:
                print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                    'ERROR :' + str(e))
        else:
            print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                  'Unable to delete Null in database.')
            self.openDialog('ไม่สามารถลบหมายเลขว่างได้')
        conn.close()
        self.loadData()

    def cfDelete(self, q_number):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("ยืนยันที่จะลบหมายเลข : " + q_number)
        #msg.setInformativeText("ยืนยันที่จะลบหมายเลข : " + q_number)
        msg.setWindowTitle("แจ้งเตือน")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok |
                               QtWidgets.QMessageBox.Cancel)
        retval = msg.exec_()
        print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
              "value of pressed message box button:", retval)
        return(retval)

    def searchData(self):
        temp = self.lineEdit.text()
        totleRow = self.tableWidget.rowCount()
        foundStatus = False
        #print(foundStatus)
        if temp != '':
            try:
                for i in range(totleRow):
                    if self.tableWidget.item(i,1).text() == temp:
                        foundStatus = True   
                        break
                    else:
                        foundStatus = False                      
                if foundStatus == True:
                    self.tableWidget.selectRow(i)
                else:
                    print(str(time.strftime("%H:%M:%S : ", time.localtime())
                              ) + 'Can not find number in table.')
                    self.openDialog('ไม่พบหมายเลขที่ต้องการ')
            except(Error) as e:
                print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                        'ERROR :' + str(e))
        else:
            print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                  'Got Null value on LineEdit ,Unable search Null in table.')
            self.openDialog('ไม่สามารถค้นหมายเลขว่างได้')

    def getCellPosition(self):
        pass
        
    def printInfo(self):
        cPosition = (int(self.tableWidget.currentColumn()))
        rPosition = (int(self.tableWidget.currentRow()))
        print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
              'Row position : ' + str(rPosition))
        print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
              'Column position : ' + str(cPosition))
        temp = self.tableWidget.item(rPosition,cPosition).text()
        print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
              'Data from cell : ' + temp)

    def paintTable(self):
        totalRow = self.tableWidget.rowCount()       
        for i in range(totalRow):
            if self.tableWidget.item(i,4).text() == '0':
                self.tableWidget.item(i, 4).setBackground(
                    QtGui.QColor('orange'))
            else:
                # self.tableWidget.item(i, 4).setBackground(
                #     QtGui.QColor('green'))
                pass

    def openDialog(self,message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('แจ้งเตือน')
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message + str(time.strftime(" @ %H:%M:%S ", time.localtime())))
        msg.exec_()

    def refreshTable(self):
        conn = sqlite3.Connection('ex1')
        try:
            cfCode = self.cfRefresh()
            if cfCode == 1024:
                query = 'DELETE FROM queue'
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                    'Refresh(TRUNCATE) queue table in database success.')
                self.openDialog('เคลียร์ตารางเรียบร้อยแล้ว')
            else:
                pass
        except(Error) as e:
            print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                  'ERROR :' + str(e))
        conn.close()
        self.loadData()

    def cfRefresh(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("ยืนยันที่จะเคลียร์ตาราง")
        #msg.setInformativeText("ยืนยันที่จะลบหมายเลข : " + q_number)
        msg.setWindowTitle("แจ้งเตือน")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok |
                               QtWidgets.QMessageBox.Cancel)
        retval = msg.exec_()
        print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
              "value of pressed message box button:", retval)
        return(retval)

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
        self.btn_call.setStyleSheet('background-color: green')
        self.btn_add = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add.setGeometry(QtCore.QRect(10, 380, 89, 71))
        self.btn_add.setStyleSheet("")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setStyleSheet('background-color: yellow')
        self.btn_delete = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete.setGeometry(QtCore.QRect(120, 380, 89, 71))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setStyleSheet('background-color: red')
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(230, 380, 89, 71))
        self.btn_search.setObjectName("btn_search")
        self.btn_search.setStyleSheet('background-color: blue')
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 681, 311))
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnWidth(1,200)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.setColumnHidden(0,True)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 334, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(335, 334, 121, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setEnabled(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menubar.setObjectName("menubar")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # self.action_Invite_window = QtWidgets.QAction(MainWindow)
        # self.action_Invite_window.setObjectName("action_Invite_window")
        # self.actionPlace_windows = QtWidgets.QAction(MainWindow)
        # self.actionPlace_windows.setObjectName("actionPlace_windows")
        # self.actionini_py = QtWidgets.QAction(MainWindow)
        # self.actionini_py.setObjectName("actionini_py")
        # self.menuSetting.addAction(self.action_Invite_window)
        # self.menuSetting.addAction(self.actionPlace_windows)
        # self.menuSetting.addAction(self.actionini_py)
        # self.menubar.addAction(self.menuSetting.menuAction())
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

        self.lineEdit.setFocus()
        self.loadData()
        self.btn_add.clicked.connect(self.writeData)
        self.btn_delete.clicked.connect(self.deleteData)
        self.btn_search.clicked.connect(self.searchData)
        self.actionDrop_tablel.triggered.connect(self.refreshTable)
        self.tableWidget.cellDoubleClicked.connect(self.printInfo)
        #self.tableWidget.sortByColumn()
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_call.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อเรียกคิวที่เลือกจากตารางคิว</p></body></html>"))
        self.btn_call.setText(_translate("MainWindow", "CALL"))
        self.btn_add.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อเปิดเมนูการเพิ่มคิวด้วยตัวเอง</p></body></html>"))
        self.btn_add.setText(_translate("MainWindow", "M-ADD"))
        self.btn_delete.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อลบคิวที่ป้อนค่าผิดออกจากตารางคิว</p></body></html>"))
        self.btn_delete.setText(_translate("MainWindow", "DELETE"))
        self.btn_search.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>คลิ๊กเพื่อโหลดตารางคิวใหม่</p></body></html>"))
        self.btn_search.setText(_translate("MainWindow", "SEARCH"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Number"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Enter time"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Call time"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Status"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Destination"))
        # self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        # self.action_Invite_window.setText(_translate("MainWindow", "Invite setting"))
        # self.actionPlace_windows.setText(_translate("MainWindow", "Place setting"))
        # self.actionini_py.setText(_translate("MainWindow", "ini.py"))
        self.menuSetting.setTitle(_translate("MainWindow", "Setting"))
        self.action_Invite_window.setText(
            _translate("MainWindow", "Invite sentence"))
        self.actionPlace_windows.setText(
            _translate("MainWindow", "Place sentence"))
        self.actionini_py.setText(_translate("MainWindow", "ini.py"))
        self.actionDestination.setText(
            _translate("MainWindow", "Destination setting"))
        self.actionDrop_tablel.setText(_translate("MainWindow", "Clear tablel"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    MainWindow.show()
    
    sys.exit(app.exec_())
