from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import time
import numpy as np
import PIL
import pyautogui
import os


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Register')
        self.setWindowIcon(QIcon('reg_file_icon.jpg'))
        self.setFixedSize(560, 731)

        self.al = '0'.zfill(8)
        self.bl = '0'.zfill(8)
        self.cl = '0'.zfill(8)
        self.dl = '0'.zfill(8)

        self.ax = '0'.zfill(8)
        self.bx = '0'.zfill(8)
        self.cx = '0'.zfill(8)
        self.dx = '0'.zfill(8)

        self.click = 0

        self.register1 = QLabel(self)
        self.register1.setGeometry(30, 400, 91, 31)
        self.register1.setText('Register1:')

        self.register2 = QLabel(self)
        self.register2.setGeometry(30, 440, 91, 31)
        self.register2.setText('Register2:')

        self.register3 = QLabel(self)
        self.register3.setGeometry(30, 480, 91, 31)
        self.register3.setText('Register3:')

        self.register4 = QLabel(self)
        self.register4.setGeometry(30, 520, 91, 31)
        self.register4.setText('Register4:')

        self.name_nh = QLabel(self)
        self.name_nh.setGeometry(120, 360, 91, 31)
        self.name_nh.setText('NH')

        self.name_nl = QLabel(self)
        self.name_nl.setGeometry(220, 360, 91, 31)
        self.name_nl.setText('NL')

        self.name_comands = QLabel(self)
        self.name_comands.setGeometry(30, 330, 200, 31)
        self.name_comands.setText('MOV/ADD/SUB NL/NX NUMBER')

        self.NHA = QLabel(self)
        self.NHA.setGeometry(120, 400, 91, 31)
        self.NHA.setText(self.ax)

        self.NHB = QLabel(self)
        self.NHB.setGeometry(120, 440, 91, 31)
        self.NHB.setText(self.bx)

        self.NHC = QLabel(self)
        self.NHC.setGeometry(120, 480, 91, 31)
        self.NHC.setText(self.cx)

        self.NHD = QLabel(self)
        self.NHD.setGeometry(120, 520, 91, 31)
        self.NHD.setText(self.dx)

        self.NLA = QLabel(self)
        self.NLA.setGeometry(220, 400, 91, 31)
        self.NLA.setText(self.al)

        self.NLB = QLabel(self)
        self.NLB.setGeometry(220, 440, 91, 31)
        self.NLB.setText(self.bl)

        self.NLC = QLabel(self)
        self.NLC.setGeometry(220, 480, 91, 31)
        self.NLC.setText(self.cl)

        self.NLD = QLabel(self)
        self.NLD.setGeometry(220, 520, 91, 31)
        self.NLD.setText(self.dl)

        self.number = QLabel(self)
        self.number.setGeometry(230, 330, 121, 31)

        self.number_choose = QLabel(self)
        self.number_choose.setGeometry(230, 60, 121, 31)

        self.history_register = QTextEdit(self)
        self.history_register.setGeometry(220, 210, 121, 121)

        self.start = QPushButton('Start program', self)
        self.start.setGeometry(30, 20, 170, 41)
        self.start.clicked.connect(self.display_text_all)

        self.start_by_step = QPushButton('Step program', self)
        self.start_by_step.setGeometry(220, 20, 120, 41)
        self.start_by_step.clicked.connect(self.step_program)

        self.choose_line = QPushButton('Choose line', self)
        self.choose_line.setGeometry(220, 90, 120, 31)
        self.choose_line.clicked.connect(self.on_click)

        self.clear = QPushButton('Clear program', self)
        self.clear.setGeometry(220, 130, 120, 31)
        self.clear.clicked.connect(self.clear_comands)

        self.register_hist = QPushButton('History program', self)
        self.register_hist.setGeometry(220, 170, 120, 31)
        self.register_hist.clicked.connect(self.show_history)

        self.save = QPushButton('Save program', self)
        self.save.setGeometry(30, 570, 141, 41)
        self.save.clicked.connect(self.save_text_file)

        self.load = QPushButton('Load program', self)
        self.load.setGeometry(200, 570, 141, 41)
        self.load.clicked.connect(self.load_text_file)

        self.comand_line = QTextEdit(self)
        self.comand_line.setGeometry(30, 70, 171, 261)

        self.name_file = QTextEdit(self)
        self.name_file.setGeometry(30, 620, 311, 41)

        self.info_int = QLabel(self)
        self.info_int.setGeometry(360, 70, 171, 261)

        self.dos = ['00H 21H', '2AH 21H', '2CH 21H', '01H 21H', '02H 21H', '05H 05H', '03H 10H', '00H 40H', '00H 3FH',
                    '00H 41H']
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(350, 20, 171, 40)
        self.combo_box.setEditable(True)
        self.combo_box.addItems(self.dos)
        self.combo_box.activated[str].connect(self.on_clicked)

        self.information = QLabel("Information about Interrup:", self)
        self.information.setGeometry(350, 50, 160, 50)

        self.information_line = QTextEdit(self)
        self.information_line.setGeometry(350, 100, 171, 231)

        self.int_asci = QLabel("Output/Input of Interrup:", self)
        self.int_asci.setGeometry(350, 350, 160, 50)

        self.int_line = QTextEdit(self)
        self.int_line.setGeometry(350, 400, 171, 141)

        self.show()

    def on_clicked(self, value):
        if value == '00H 21H':
            text = 'Zakonczenie programu.'
            self.information_line.setPlainText(text)

        elif value == '2AH 21H':
            text = 'Pobieranie aktualnej daty.\n' \
                   'AL = dzień tygodnia\n' \
                   'CL = rok\n' \
                   'DH = miesiąc'
            self.information_line.setPlainText(text)

        elif value == '2CH 21H':
            text = 'Pobierz czas.\n' \
                   'CH = godzina\n' \
                   'CL = minuta\n' \
                   'DH = sekunda'
            self.information_line.setPlainText(text)

        elif value == '01H 21H':
            text = 'Czytanie znaku z echem. Funkcja ta pobiera znak w standardowym strumieniu wejściowym. Przed ' \
                   'wykonaniem funkcji wpisz znak do strumienia wejsciowego.Funkcja ' \
                   'kopiuje go do standardowego strumienia wyjściowego. Po odebraniu znaku, funkcja w rejestrze AL ' \
                   'zwraca kod ASCII tego znaku. '
            self.information_line.setPlainText(text)

        elif value == '02H 21H':
            text = 'Wypisywanie znaku. Funkcja ta przesyła znak, którego kod ASCII znajduje się (w formie binarnej)  ' \
                   'w rejestrze DL do standardowego strumienia wyjściowego. '
            self.information_line.setPlainText(text)

        elif value == '05H 05H':
            text = 'Dokonanie zrzutu ekranu i zapisanie go w folderze programu.'
            self.information_line.setPlainText(text)

        elif value == '03H 10H':
            text = 'Wypisanie aktualnej pozycji kursora.'
            self.information_line.setPlainText(text)

        elif value == '00H 40H':
            text = 'Zapisanie do pliku (file.txt), w naszym programie zapisujemy historie programu.'
            self.information_line.setPlainText(text)

        elif value == '00H 3FH':
            text = 'Wczytanie z pliku (file.txt). Wczytuje do strumienia wyjściowego.'
            self.information_line.setPlainText(text)

        else:
            text = 'Usuniecie pliku (file.txt)'
            self.information_line.setPlainText(text)

    def print_information(self):
        role = self.combo.currentData()
        self.info_int.setText(role)

    def on_click(self):
        self.click += 1
        self.number_choose.setText('Choose line: ' + f'{self.click}')

    def load_text_file(self):
        self.load_file = self.name_file.toPlainText()
        file = open(self.load_file, "r+")
        self.comand_line.setPlainText(file.read())

    def save_text_file(self):
        self.text_comands = self.comand_line.toPlainText()
        self.save_file = self.name_file.toPlainText()
        file = open(self.save_file, "w")
        file.write(self.text_comands)
        file.close()

    def show_history(self):
        self.text_comands = self.comand_line.toPlainText()
        self.list_words = self.text_comands.split("\n")
        self.number.setText('Ilosc linii: ' + str(len(self.list_words)))
        self.history_register.setPlainText(self.text_comands)

    def clear_comands(self):
        self.comand_line.clear()
        self.al = '0'.zfill(8)
        self.bl = '0'.zfill(8)
        self.cl = '0'.zfill(8)
        self.dl = '0'.zfill(8)

        self.ax = '0'.zfill(8)
        self.bx = '0'.zfill(8)
        self.cx = '0'.zfill(8)
        self.dx = '0'.zfill(8)

        self.NLA.setText(self.al.zfill(8))
        self.NLB.setText(self.bl.zfill(8))
        self.NLC.setText(self.cl.zfill(8))
        self.NLD.setText(self.dl.zfill(8))
        self.NHA.setText(self.ax.zfill(8))
        self.NHB.setText(self.bx.zfill(8))
        self.NHC.setText(self.cx.zfill(8))
        self.NHD.setText(self.dx.zfill(8))

    def display_text_all(self):
        move = 'MOV'
        add = 'ADD'
        sub = 'SUB'
        int_value = 'INT'
        nl = ['AL', 'BL', 'CL', 'DL']
        nx = ['AX', 'BX', 'CX', 'DX']
        dos = ['00H 21H', '2AH 21H', '2CH 21H', '01H 21H', '02H 21H', '05H 05H', '03H 10H', '00H 40H', '00H 3FH',
               '00H 41H']

        self.text_comands = self.comand_line.toPlainText()
        self.list_words = self.text_comands.split("\n")

        self.number.setText('Number of lines: ' + f'{len(self.list_words)}')

        for i in range(len(self.list_words)):
            if move in self.list_words[i]:
                if nl[0] in self.list_words[i]:
                    self.al = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.NLA.setText(self.al.zfill(8))

                elif nl[1] in self.list_words[i]:
                    self.bl = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.NLB.setText(self.bl.zfill(8))

                elif nl[2] in self.list_words[i]:
                    self.cl = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.NLC.setText(self.cl.zfill(8))

                elif nl[3] in self.list_words[i]:
                    self.dl = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.NLD.setText(self.dl.zfill(8))

                elif nx[0] in self.list_words[i]:
                    self.ax = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.NHA.setText(self.ax.zfill(8))

                elif nx[1] in self.list_words[i]:
                    self.bx = str(format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b"))
                    self.NHB.setText(self.bx.zfill(8))

                elif nx[2] in self.list_words[i]:
                    self.cx = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.NHC.setText(self.cx.zfill(8))
                    self.history_register.setPlainText(self.list_words[i])

                elif nx[3] in self.list_words[i]:
                    self.dx = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.NHD.setText(self.dx.zfill(8))

            elif add in self.list_words[i]:
                if nl[0] in self.list_words[i]:
                    self.al_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.al = format((int(self.al, 2) + int(self.al_add, 2)), "b")
                    self.NLA.setText(self.al.zfill(8))

                elif nl[1] in self.list_words[i]:
                    self.bl_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.bl = format((int(self.bl, 2) + int(self.bl_add, 2)), "b")
                    self.NLB.setText(self.bl.zfill(8))

                elif nl[2] in self.list_words[i]:
                    self.cl_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.cl = format((int(self.cl, 2) + int(self.cl_add, 2)), "b")
                    self.NLC.setText(self.cl.zfill(8))

                elif nl[3] in self.list_words[i]:
                    self.dl_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.dl = format((int(self.dl, 2) + int(self.dl_add, 2)), "b")
                    self.NLD.setText(self.dl.zfill(8))

                elif nx[0] in self.list_words[i]:
                    self.ax_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.ax = format((int(self.ax, 2) + int(self.ax_add, 2)), "b")
                    self.NHA.setText(self.ax.zfill(8))

                elif nx[1] in self.list_words[i]:
                    self.bx_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.bx = format((int(self.bx, 2) + int(self.bx_add, 2)), "b")
                    self.NHB.setText(self.bx.zfill(8))

                elif nx[2] in self.list_words[i]:
                    self.cx_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.cx = format((int(self.cx, 2) + int(self.cx_add, 2)), "b")
                    self.NHC.setText(self.cx.zfill(8))

                elif nx[3] in self.list_words[i]:
                    self.dx_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.dx = format((int(self.dx, 2) + int(self.dx_add, 2)), "b")
                    self.NHD.setText(self.dx.zfill(8))

            elif sub in self.list_words[i]:
                if nl[0] in self.list_words[i]:
                    self.al_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.al = format((int(self.al, 2) - int(self.al_sub, 2)), "b")
                    self.NLA.setText(self.al.zfill(8))

                elif nl[1] in self.list_words[i]:
                    self.bl_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.bl = format((int(self.bl, 2) - int(self.bl_sub, 2)), "b")
                    self.NLB.setText(self.bl.zfill(8))

                elif nl[2] in self.list_words[i]:
                    self.cl_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.cl = format((int(self.cl, 2) - int(self.cl_sub, 2)), "b")
                    self.NLC.setText(self.cl.zfill(8))

                elif nl[3] in self.list_words[i]:
                    self.dl_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.dl = format((int(self.dl, 2) - int(self.dl_sub, 2)), "b")
                    self.NLD.setText(self.dl.zfill(8))

                elif nx[0] in self.list_words[i]:
                    self.ax_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.ax = format((int(self.ax, 2) - int(self.ax_sub, 2)), "b")
                    self.NHA.setText(self.ax.zfill(8))

                elif nx[1] in self.list_words[i]:
                    self.bx_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.bx = format((int(self.bx, 2) - int(self.bx_sub, 2)), "b")
                    self.NHB.setText(self.bx.zfill(8))

                elif nx[2] in self.list_words[i]:
                    self.cx_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.cx = format((int(self.cx, 2) - int(self.cx_sub, 2)), "b")
                    self.NHC.setText(self.cx.zfill(8))

                elif nx[3] in self.list_words[i]:
                    self.dx_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                    self.dx = format((int(self.dx, 2) - int(self.dx_sub, 2)), "b")
                    self.NHD.setText(self.dx.zfill(8))

            elif int_value in self.list_words[i]:
                if dos[0] in self.list_words[i]:
                    sys.exit(app.exec_())
                elif dos[1] in self.list_words[i]:
                    self.year = time.strftime("%Y", time.localtime())
                    self.cl_add = format(int(''.join(filter(str.isdigit, self.year))), "b")
                    self.cl = format((int(self.cl, 2) + int(self.cl_add, 2)), "b")
                    self.NLC.setText(self.cl.zfill(8))

                    self.month = time.strftime("%m", time.localtime())
                    self.dx_add = format(int(''.join(filter(str.isdigit, self.month))), "b")
                    self.dx = format((int(self.dx, 2) + int(self.dx_add, 2)), "b")
                    self.NHD.setText(self.dx.zfill(8))

                    self.day = time.strftime("%d", time.localtime())
                    self.dl_add = format(int(''.join(filter(str.isdigit, self.day))), "b")
                    self.dl = format((int(self.dl, 2) + int(self.dl_add, 2)), "b")
                    self.NLD.setText(self.dl.zfill(8))

                elif dos[2] in self.list_words[i]:
                    self.hour = time.strftime("%H", time.localtime())
                    self.cx_add = format(int(''.join(filter(str.isdigit, self.hour))), "b")
                    self.cx = format((int(self.cx, 2) + int(self.cx_add, 2)), "b")
                    self.NHC.setText(self.cx.zfill(8))

                    self.minute = time.strftime("%M", time.localtime())
                    self.cl_add = format(int(''.join(filter(str.isdigit, self.minute))), "b")
                    self.cl = format((int(self.cl, 2) + int(self.cl_add, 2)), "b")
                    self.NLC.setText(self.cl.zfill(8))

                    self.seconds = time.strftime("%S", time.localtime())
                    self.dx_add = format(int(''.join(filter(str.isdigit, self.seconds))), "b")
                    self.dx = format((int(self.dx, 2) + int(self.dx_add, 2)), "b")
                    self.NHD.setText(self.dx.zfill(8))

                elif dos[3] in self.list_words[i]:
                    self.sign = self.int_line.toPlainText()
                    self.binary_sign = ''.join(format(ord(self.sign), '08b'))
                    self.al = format((int(self.al, 2) + int(self.binary_sign, 2)), "b")
                    self.NLA.setText(self.al.zfill(8))

                elif dos[4] in self.list_words[i]:
                    self.from_dl = self.dl
                    bin_data = int(self.dl, 2)
                    str_data = bin_data.to_bytes((bin_data.bit_length() + 7) // 8, 'big').decode()
                    self.int_line.setPlainText(str_data)

                elif dos[5] in self.list_words[i]:
                    image = pyautogui.screenshot()
                    image.save('image.jpg')

                elif dos[6] in self.list_words[i]:
                    position = str(pyautogui.position())
                    self.int_line.setPlainText(position)

                elif dos[7] in self.list_words[i]:
                    self.text = self.history_register.toPlainText()
                    file = open('file.txt', "w")
                    file.write(self.text)
                    file.close()

                elif dos[8] in self.list_words[i]:
                    self.text = self.history_register.toPlainText()
                    if os.path.exists('file.txt'):
                        file = open('file.txt', "r+")
                        self.int_line.setPlainText(file.read())
                    else:
                        pass

                elif dos[9] in self.list_words[i]:
                    if os.path.exists('file.txt'):
                        os.remove('file.txt')
                    else:
                        pass

    def step_program(self):
        move = 'MOV'
        add = 'ADD'
        sub = 'SUB'
        int_value = 'INT'

        nl = ['AL', 'BL', 'CL', 'DL']
        nx = ['AX', 'BX', 'CX', 'DX']
        dos = ['00H 21H', '2AH 21H', '2CH 21H', '01H 21H', '02H 21H', '05H 05H', '03H 10H', '00H 40H', '00H 3FH',
               '00H 41H']

        i = self.click - 1
        self.text_comands = self.comand_line.toPlainText()
        self.list_words = self.text_comands.split("\n")

        if move in self.list_words[i]:
            if nl[0] in self.list_words[i]:
                self.al = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.NLA.setText(self.al.zfill(8))

            elif nl[1] in self.list_words[i]:
                self.bl = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.NLB.setText(self.bl.zfill(8))

            elif nl[2] in self.list_words[i]:
                self.cl = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.NLC.setText(self.cl.zfill(8))

            elif nl[3] in self.list_words[i]:
                self.dl = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.NLD.setText(self.dl.zfill(8))

            elif nx[0] in self.list_words[i]:
                self.ax = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.NHA.setText(self.ax.zfill(8))

            elif nx[1] in self.list_words[i]:
                self.bx = str(format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b"))
                self.NHB.setText(self.bx.zfill(8))

            elif nx[2] in self.list_words[i]:
                self.cx = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.NHC.setText(self.cx.zfill(8))
                self.history_register.setPlainText(self.list_words[i])

            elif nx[3] in self.list_words[i]:
                self.dx = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.NHD.setText(self.dx.zfill(8))

        elif add in self.list_words[i]:
            if nl[0] in self.list_words[i]:
                self.al_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.al = format((int(self.al, 2) + int(self.al_add, 2)), "b")
                self.NLA.setText(self.al.zfill(8))

            elif nl[1] in self.list_words[i]:
                self.bl_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.bl = format((int(self.bl, 2) + int(self.bl_add, 2)), "b")
                self.NLB.setText(self.bl.zfill(8))

            elif nl[2] in self.list_words[i]:
                self.cl_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.cl = format((int(self.cl, 2) + int(self.cl_add, 2)), "b")
                self.NLC.setText(self.cl.zfill(8))

            elif nl[3] in self.list_words[i]:
                self.dl_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.dl = format((int(self.dl, 2) + int(self.dl_add, 2)), "b")
                self.NLD.setText(self.dl.zfill(8))

            elif nx[0] in self.list_words[i]:
                self.ax_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.ax = format((int(self.ax, 2) + int(self.ax_add, 2)), "b")
                self.NHA.setText(self.ax.zfill(8))

            elif nx[1] in self.list_words[i]:
                self.bx_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.bx = format((int(self.bx, 2) + int(self.bx_add, 2)), "b")
                self.NHB.setText(self.bx.zfill(8))

            elif nx[2] in self.list_words[i]:
                self.cx_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.cx = format((int(self.cx, 2) + int(self.cx_add, 2)), "b")
                self.NHC.setText(self.cx.zfill(8))

            elif nx[3] in self.list_words[i]:
                self.dx_add = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.dx = format((int(self.dx, 2) + int(self.dx_add, 2)), "b")
                self.NHD.setText(self.dx.zfill(8))

        elif sub in self.list_words[i]:
            if nl[0] in self.list_words[i]:
                self.al_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.al = format((int(self.al, 2) - int(self.al_sub, 2)), "b")
                self.NLA.setText(self.al.zfill(8))

            elif nl[1] in self.list_words[i]:
                self.bl_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.bl = format((int(self.bl, 2) - int(self.bl_sub, 2)), "b")
                self.NLB.setText(self.bl.zfill(8))

            elif nl[2] in self.list_words[i]:
                self.cl_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.cl = format((int(self.cl, 2) - int(self.cl_sub, 2)), "b")
                self.NLC.setText(self.cl.zfill(8))

            elif nl[3] in self.list_words[i]:
                self.dl_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.dl = format((int(self.dl, 2) - int(self.dl_sub, 2)), "b")
                self.NLD.setText(self.dl.zfill(8))

            elif nx[0] in self.list_words[i]:
                self.ax_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.ax = format((int(self.ax, 2) - int(self.ax_sub, 2)), "b")
                self.NHA.setText(self.ax.zfill(8))

            elif nx[1] in self.list_words[i]:
                self.bx_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.bx = format((int(self.bx, 2) - int(self.bx_sub, 2)), "b")
                self.NHB.setText(self.bx.zfill(8))

            elif nx[2] in self.list_words[i]:
                self.cx_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.cx = format((int(self.cx, 2) - int(self.cx_sub, 2)), "b")
                self.NHC.setText(self.cx.zfill(8))

            elif nx[3] in self.list_words[i]:
                self.dx_sub = format(int(''.join(filter(str.isdigit, self.list_words[i]))), "b")
                self.dx = format((int(self.dx, 2) - int(self.dx_sub, 2)), "b")
                self.NHD.setText(self.dx.zfill(8))

        elif int_value in self.list_words[i]:
            if dos[0] in self.list_words[i]:
                sys.exit(app.exec_())
            elif dos[1] in self.list_words[i]:
                self.year = time.strftime("%Y", time.localtime())
                self.cl_add = format(int(''.join(filter(str.isdigit, self.year))), "b")
                self.cl = format((int(self.cl, 2) + int(self.cl_add, 2)), "b")
                self.NLC.setText(self.cl.zfill(8))

                self.month = time.strftime("%m", time.localtime())
                self.dx_add = format(int(''.join(filter(str.isdigit, self.month))), "b")
                self.dx = format((int(self.dx, 2) + int(self.dx_add, 2)), "b")
                self.NHD.setText(self.dx.zfill(8))

                self.day = time.strftime("%d", time.localtime())
                self.dl_add = format(int(''.join(filter(str.isdigit, self.day))), "b")
                self.dl = format((int(self.dl, 2) + int(self.dl_add, 2)), "b")
                self.NLD.setText(self.dl.zfill(8))

            elif dos[2] in self.list_words[i]:
                self.hour = time.strftime("%H", time.localtime())
                self.cx_add = format(int(''.join(filter(str.isdigit, self.hour))), "b")
                self.cx = format((int(self.cx, 2) + int(self.cx_add, 2)), "b")
                self.NHC.setText(self.cx.zfill(8))

                self.minute = time.strftime("%M", time.localtime())
                self.cl_add = format(int(''.join(filter(str.isdigit, self.minute))), "b")
                self.cl = format((int(self.cl, 2) + int(self.cl_add, 2)), "b")
                self.NLC.setText(self.cl.zfill(8))

                self.seconds = time.strftime("%S", time.localtime())
                self.dx_add = format(int(''.join(filter(str.isdigit, self.seconds))), "b")
                self.dx = format((int(self.dx, 2) + int(self.dx_add, 2)), "b")
                self.NHD.setText(self.dx.zfill(8))

            elif dos[3] in self.list_words[i]:
                self.sign = self.int_line.toPlainText()
                self.binary_sign = ''.join(format(ord(self.sign), '08b'))
                self.al = format((int(self.al, 2) + int(self.binary_sign, 2)), "b")
                self.NLA.setText(self.al.zfill(8))

            elif dos[4] in self.list_words[i]:
                self.from_dl = self.dl
                bin_data = int(self.dl, 2)
                str_data = bin_data.to_bytes((bin_data.bit_length() + 7) // 8, 'big').decode()
                self.int_line.setPlainText(str_data)

            elif dos[5] in self.list_words[i]:
                image = pyautogui.screenshot()
                image.save('image.jpg')

            elif dos[6] in self.list_words[i]:
                position = str(pyautogui.position())
                self.int_line.setPlainText(position)

            elif dos[7] in self.list_words[i]:
                self.text = self.history_register.toPlainText()
                file = open('file.txt', "w")
                file.write(self.text)
                file.close()

            elif dos[8] in self.list_words[i]:
                self.text = self.history_register.toPlainText()
                if os.path.exists('file.txt'):
                    file = open('file.txt', "r+")
                    self.int_line.setPlainText(file.read())
                else:
                    pass

            elif dos[9] in self.list_words[i]:
                if os.path.exists('file.txt'):
                    os.remove('file.txt')
                else:
                    pass


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
