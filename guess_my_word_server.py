import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QWidget, QTabWidget, QInputDialog, QLabel, QGridLayout, QCheckBox, QSlider, QProgressBar, QCalendarWidget, QMessageBox
from PyQt5.QtCore import Qt
import time

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(("localhost",10000))
main_socket.setblocking(False)
main_socket.listen(2)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow2")
        MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 20, 381, 191))
        self.label.setStyleSheet("font: 87 14pt \"Arial\";")
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(300, 300, 381, 100))
        self.label2.setStyleSheet("font: 87 14pt \"Arial\";")
        self.label2.setObjectName("label2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Онлайн крокодил | Игрок 1"))
        self.label.setText(_translate("MainWindow", "Добро пожаловать в игру \"Крокодил\""))
        self.label2.setText(_translate("MainWindow", "Ожидание игрока 2..."))
        
class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.points2 = 0
        self.points = 0
        self.client_socket = None
        self.myUI()
        
    def myUI(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_connection)
        self.timer.start(1000)

    def check_connection(self):
        try:
            self.client_socket, _ = main_socket.accept()
            self.client_socket.setblocking(False)
            self.timer.stop()
            self.buttonClicked_2()
        except BlockingIOError:
            pass
        except Exception as e:
            print(f"Ошибка при проверке подключения: {e}")
        
    def buttonClicked_2(self):
        w = QWidget()
        self.label = QtWidgets.QLabel("Игрок 2 вводит слово\nОжидайте...", w)
        self.label.setFont(QtGui.QFont("Arial", 14))
        self.label.move(100, 150)
        self.setCentralWidget(w)
        self.waiting()

    def waiting(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.wait_msg)
        self.timer.start(1000)
            

    def wait_msg(self):
        try:
            if self.client_socket is None:
                print("Попытка принять соединение")
                try:
                    self.client_socket, _ = main_socket.accept()
                    self.client_socket.settimeout(1.0)
                    print("Соединение установлено")
                except BlockingIOError:
                    return 
                except Exception as e:
                    print(f"Ошибка accept: {e}")
                    return

            try:
                print("Ожидание данных...")
                self.data = self.client_socket.recv(1024).decode()
                if self.data:
                    print(f"Получены данные: {self.data}")
                    self.data1 = self.data.split("_")
                    self.timer.stop()
                    if self.data1[0] == "123456":
                        self.win2()
                    if self.data1[0]=="654321":
                        self.win1()
                    self.player2()
            except socket.timeout:
                print("Таймаут ожидания данных")
            except Exception as e:
                print(f"Ошибка чтения: {e}")

        except Exception as e:
            print(f"Общая ошибка: {e}")
            if self.client_socket:
                pass
    def player2(self):
        self.w = QWidget()
        self.label = QtWidgets.QLabel(self.data1[0][0].upper()+" _ _ _ _", self.w)
        self.label.setGeometry(340, 0,1000,50)
        self.label.setFont(QtGui.QFont("Arial", 14))
        self.setCentralWidget(self.w)
        self.label2 = QtWidgets.QLabel(self.data1[1], self.w)
        self.label2.setFont(QtGui.QFont("Arial", 14))
        self.label2.setGeometry(100,100,600,100)
        self.label2.setWordWrap(True)
        self.text = QtWidgets.QTextEdit("Введите слово", self.w)
        self.text.setGeometry(QtCore.QRect(100, 200, 600, 60))
        self.btn = QPushButton("Проверить",self.w)
        self.btn.setGeometry(340,280,100,60)
        self.ltr = 1
        self.btn.clicked.connect(self.checkans)

    def buttonClicked(self):
        w = QWidget()
        try:
            self.timer.stop()
        except:
            pass
        self.label = QtWidgets.QLabel("Загадайте слово из 5 букв", w)
        self.label.setFont(QtGui.QFont("Arial", 14))
        self.label.setGeometry(280,30,500,50)
        self.text = QtWidgets.QTextEdit("Введите слово", w)
        self.text.setGeometry(QtCore.QRect(100, 100, 600, 60))
        self.btn = QtWidgets.QPushButton(w)
        self.btn.setGeometry(QtCore.QRect(340,280,100,60))
        self.text2 = QtWidgets.QTextEdit("Введите загадку", w)
        self.text2.setGeometry(QtCore.QRect(100, 180, 600, 60))
        self.btn.setText("Отправить")
        self.setCentralWidget(w)
        self.btn.clicked.connect(self.check_word)

    def check_word(self):
        if len(self.text.toPlainText()) != 5:
            self.label.setText("Слово должно состоять из 5 букв")
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.buttonClicked)
            self.timer.start(4000)
        else:
            self.send_word()

    def send_word(self):
        print(f"{self.text.toPlainText()}_{self.text2.toPlainText()}")
        self.client_socket.send(f"{self.text.toPlainText()}_{self.text2.toPlainText()}".encode())
        w = QWidget()
        self.label = QtWidgets.QLabel("Игрок 2 отгадывает слово\nОжидайте...", w)
        self.label.setFont(QtGui.QFont("Arial", 14))
        self.label.move(100, 150)
        self.setCentralWidget(w)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.wait_msg2)
        self.timer.start(1000)

    def wait_msg2(self):
            try:
                data = self.client_socket.recv(1024).decode()
                if data:
                    print(f"Получены данные: {data}")
                    self.data1 = data.split("_")
                    self.points2 = int(self.data1[0])
                    self.points = int(self.data1[2])
                    self.timer.stop()
                    self.client_socket.setblocking(True)
                    if self.data1[0] == "123456":
                        self.win2()
                    if self.data1[0]=="654321":
                        self.win1()
                    self.label.setText(self.data1[1]+"\nВаши баллы: "+self.data1[0])
                    self.timer = QtCore.QTimer()
                    self.timer.timeout.connect(self.buttonClicked_2)
                    self.timer.start(4000)
            except BlockingIOError:
                pass
            except socket.timeout:
                print("Таймаут ожидания данных")
            except Exception as e:
                print(f"Ошибка чтения: {e}")
                self.timer.stop()

    def checkans(self):
        if self.text.toPlainText().lower() != self.data1[0].lower():
            self.ltr+=1
            a = ""
            b = ""
            for i in range(self.ltr):
                a = (a+self.data1[0][i].upper())
            for i in range(5-self.ltr):
                b = (b+"_ ")
            self.label.setText(a+b)
            self.points+=1
            if 5 - self.ltr == 0:
                self.label.setText("Вы не отгадали слово") 
                self.client_socket.send(f"{self.points}_{"Ваше слово не отгадали"}_{self.points2}".encode())
                QtCore.QTimer.singleShot(3000,lambda:self.buttonClicked())
        else:
            self.points-=1
            self.points2+=2
            self.label.setText(self.data1[0])
            self.label2.setText("Слово отгаданно!")
            self.client_socket.send(f"{self.points}_{"Ваше слово отгадали"}_{self.points2}".encode())
            QtCore.QTimer.singleShot(3000,lambda:self.buttonClicked())
        if self.points2 >= 5:
            self.label2.setText("Победил игрок 1")
            self.win1()
        if self.points >= 5:
            self.label2.setText("Победил игрок 2")
            self.win2()

    def win1(self):
        self.client_socket.send(f"{"654321"}_Ваше слово отгадали_{self.points}".encode())
        msg_box = QMessageBox()
        msg_box.setText("Победил игрок 1!")
        msg_box.setWindowTitle("Победа")
        msg_box.setStandardButtons(QMessageBox.Ok)
        if msg_box.exec() == QMessageBox.Ok:
            exit()

    def win2(self):
        self.client_socket.send(f"{"123456"}_Ваше слово отгадали_{self.points}".encode())
        msg_box = QMessageBox()
        msg_box.setText("Победил игрок 2!")
        msg_box.setWindowTitle("Поражение")
        msg_box.setStandardButtons(QMessageBox.Ok)
        if msg_box.exec() == QMessageBox.Ok:
            exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())