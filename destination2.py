from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQueryModel, QSqlQuery, QSqlDatabase, QSqlError
from PyQt5.QtWidgets import QMessageBox
import time

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(10, 10, 250, 281))
        self.listView.setObjectName("listView")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        self.listView.setFont(font)
        self.btn_add = QtWidgets.QPushButton(Dialog)
        self.btn_add.setGeometry(QtCore.QRect(270, 50, 121, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        self.btn_add.setFont(font)
        self.btn_add.setObjectName("btn_add")
        self.btn_del = QtWidgets.QPushButton(Dialog)
        self.btn_del.setGeometry(QtCore.QRect(270, 90, 121, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        self.btn_del.setFont(font)
        self.btn_del.setObjectName("btn_del")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(270, 10, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.loadData()

        self.btn_add.clicked.connect(self.insertData)
        self.btn_del.clicked.connect(self.deleteData)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Destination setting"))
        self.btn_add.setText(_translate("Dialog", "Add"))
        self.btn_del.setText(_translate("Dialog", "Delete"))

    def loadData(self):
        self.lineEdit.clear()
        self.lineEdit.setFocus()

        self.desModel = QSqlQueryModel()
        selectQuery = QSqlQuery()
        selectQuery.prepare('SELECT des_name FROM destination')
        print('QUERY = ' + str(selectQuery.lastQuery()))

        if selectQuery.exec():
            self.desModel.setQuery(selectQuery)
            print('SELECT des_name COMPLETE')
            self.listView.setModel(self.desModel)
        else:
            print('SELECT FALSE = ' + selectQuery.lastError().text())

    def insertData(self):
        des_name = self.lineEdit.text()
        # des_name ต้องไม่ใช่ค่าเว้นวรรค และ ต้องไม่ใช่ค่าว่าง
        if not des_name.isspace() and des_name != '':
            try:
                insertQuery = QSqlQuery()
                insertQuery.prepare("INSERT INTO destination " + "(des_name)" +
                                    "VALUES " + f"('{des_name}')")
                print('Query = ' + insertQuery.lastQuery())
                if insertQuery.exec():
                    print('INSERT COMPLETE')
                    self.showDialog('เพิ่มปลายทาง : ' + des_name + ' แล้ว')
                    self.loadData()
                else:
                    print('INSERT FALSE = ' + insertQuery.lastError().text())          
            except(QSqlError) as e:
                print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                      'ERROR :' + str(e))     
        else:
            self.showDialog('กรุณากรอกปลายทางที่จะเพิ่มก่อน')

    def deleteData(self):     
        current_row = self.listView.currentIndex()
        des_name = self.listView.model().data(current_row,0)
        
        # ถ้าไม่ได้เลือก record ให้ return
        if des_name == None:
            self.showDialog('กรุณาเลือกปลายทางที่จะลบก่อน')
            return

        des_name_inUse = False # เก็บ status ของ des_name

        # สร้าง sqlmModel ไว้สำหรับ query des_id มาเทียบกันระหว่างสองตาราง
        tempFromQueue = QSqlQueryModel()
        selectQueue = QSqlQuery()
        selectQueue.prepare('SELECT des_id FROM queue')

        tempFromDes = QSqlQueryModel()
        selectDes = QSqlQuery()
        selectDes.prepare('SELECT des_id FROM destination WHERE des_name = ' + f"'{des_name}'")

        # เก็บค่าของจากทั้งสองตารางมาตรวจสอบการซ้ำของ des_id ว่ามีการใชงานอยู่จริงหรือไม่
        # exec query ถ้าผ่านให้ setQuery
        if selectDes.exec() == True and selectQueue.exec() == True:
            tempFromDes.setQuery(selectDes)
            tempFromQueue.setQuery(selectQueue)

            # fetch more หา rowCount ของจริง
            while tempFromQueue.canFetchMore():
                tempFromQueue.fetchMore()

            # เทียบค่า des_id
            for i in range(tempFromQueue.rowCount()):
                if tempFromQueue.index(i,0).data() == tempFromDes.index(0,0).data():
                    des_name_inUse = True 
                    break
                else:
                    des_name_inUse = False

        # ตรวจสอบว่า des_name ไม่มีการใช้งานในตาราง queue
        # หากมีการใช้งาน จะไม่สามารถลบออกจาก destination ได้
        if des_name_inUse == True:
            self.showDialog(f'ปลายทาง {des_name} มีการใช้งานในตาราง ไม่สามารถลบได้')
            return

        # ยืนยันการลบด้วย code 1024
        confCode = self.confDelete(des_name)
        if confCode == 1024:
            try:
                deleteQuery = QSqlQuery()
                deleteQuery.prepare("DELETE FROM destination WHERE des_name = " + 
                                    f"('{des_name}')")
                print('Query = ' + deleteQuery.lastQuery())
                if deleteQuery.exec():
                    print('DELETE COMPLETE')
                    self.showDialog('ลบปลายทาง : ' + des_name + ' แล้ว')
                    self.loadData()
                else:
                    print('DELETE FALSE = ' + deleteQuery.lastError().text())
            except(QSqlError) as e:
                print(str(time.strftime("%H:%M:%S : ", time.localtime())) +
                      'ERROR :' + str(e))   
        else:
            print('User decided cancel delete this record.')
    
    def confDelete(self,des_name):
        # สร้าง dialog เพื่อยืนยันการลบ และ return code ยืนยันการลบด้วย code 1024
        confMsg = QtWidgets.QMessageBox()
        confMsg.setIcon(QtWidgets.QMessageBox.Critical)
        confMsg.setText('ยืนยันที่จะลบปลายทาง : ' + des_name)
        confMsg.setWindowTitle('แจ้งเตือนการลบ')
        confMsg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        reval = confMsg.exec_()
        return(reval)

    def showDialog(self,message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('แจ้งเตือน')
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
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
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
