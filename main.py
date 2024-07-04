import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow, QTableWidgetItem, QMessageBox
from addEditUI import Ui_Form
from mainUI import Ui_MainWindow

class DBSample(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.pushButton.clicked.connect(self.select_data)
        self.pushButton_2.clicked.connect(self.addEditBD)
        # По умолчанию будем выводить все данные из таблицы films
        self.textEdit.setPlainText("SELECT * FROM coffee")
        self.select_data()

    def select_data(self):
        query = self.textEdit.toPlainText()
        res = self.connection.cursor().execute(query).fetchall()
        print(res)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def addEditBD(self):
        self.second_form = SecondForm(self, "Редактирование/Добавление")
        self.second_form.show()

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()

class SecondForm(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.setupUiAddEdit(self)
        # uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection2 = sqlite3.connect("data/coffee.sqlite")
        self.pushButtonAdd.clicked.connect(self.addDataToDB)
        self.pushButtonEdit.clicked.connect(self.editDataInBD)

    def addDataToDB(self):
        ans = [''] * 7
        ans[0] = int(self.lineEdit.text())
        ans[1] = self.lineEdit_2.text()
        ans[2] = self.lineEdit_3.text()
        ans[3] = self.lineEdit_4.text()
        ans[4] = self.lineEdit_5.text()
        ans[5] = int(self.lineEdit_6.text())
        ans[6] = int(self.lineEdit_7.text())
        print(ans)
        que = """INSERT INTO coffee (Id, Name, Roasting, Grounded, Taste, Cost, Volume) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        self.connection2.cursor().execute(que, ans)
        self.connection2.commit()


    def editDataInBD(self):
        ans = [''] * 7
        ans[0] = int(self.lineEdit.text())
        ans[1] = self.lineEdit_2.text()
        ans[2] = self.lineEdit_3.text()
        ans[3] = self.lineEdit_4.text()
        ans[4] = self.lineEdit_5.text()
        ans[5] = int(self.lineEdit_6.text())
        ans[6] = int(self.lineEdit_7.text())
        print(ans)
        result = self.connection2.cursor().execute("SELECT * FROM coffee WHERE id=?",(ans[0],)).fetchall()
        print(result)
        if not result:
            QMessageBox.information(self, "Предупреждение!", "Такого ID не нашлось!")
            return
        else:
            print('Hello')
            valid = QMessageBox.question(
                self, '', "Действительно изменить данные с id " + str(ans[0]),
                QMessageBox.Yes, QMessageBox.No)
            # Если пользователь ответил утвердительно, удаляем элементы.
            # Не забываем зафиксировать изменения
            if valid == QMessageBox.Yes:
                for i in range(7):
                    if ans[i] == "":
                        ans[i] = result[0][i]
                print(ans)
                QMessageBox.information(self, "Предупреждение!", f"Данные с ID {ans[0]} изменены!")
                que = """UPDATE coffee SET Name = ?, Roasting = ?, Grounded = ?, Taste = ?, Cost = ?, Volume = ? WHERE id = ?"""
                self.connection2.cursor().execute(que, ans[1:] + [ans[0]])
                self.connection2.commit()

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection2.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())