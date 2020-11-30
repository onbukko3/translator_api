import os
import sys
import pyperclip
import requests
import time
import datetime
from PyQt5 import QtCore, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from googletrans import Translator
import clipboard
import json

def getting_auth(filename):
    dirlist = os.listdir()
    if filename in dirlist:
        auth_path = os.path.abspath(filename)
        with open(auth_path, 'r') as auth:
            auths = auth.readlines()
            data = []
            for auth in auths:
                data.append(auth.rstrip('\n'))
    return data[0], data[1]


filename = sys.argv[1]
id, secret = getting_auth(filename)

PAPAGO_USER_ID     =   id # client ID
PAPAGO_USER_SECRET =   secret # client secret
#GOOGLE_USER_ID=""
#GOOGLE_USER_SECRET=""
LANGUAGE_LIST = ["ko","en","ja",""]
text = ""
result = ""


class inputdialogdemo(QWidget):
    def __init__(self, parent = None):
        super(inputdialogdemo, self).__init__(parent)

        self.setGeometry(0,0, 700, 700)
        font = QFont()
        font.setPointSize(30)

        self.target="en"
        self.btn=QPushButton("German")
        self.btn.setCheckable(True)
        self.btn.toggle()
        self.btn.pressed.connect(self.language_selecting)

        self.btn_1=QPushButton("English")
        self.btn_1.setCheckable(True)
        self.btn_1.toggle()
        self.btn_1.pressed.connect(self.target_reset)

        layout = QVBoxLayout()
        self.le = QTextEdit()
        self.le.resize(100,300)
        self.le.setFont(font)
        self.le.setFocus()
        self.le.setTabChangesFocus(True)
        layout.addWidget(self.btn_1)
        layout.addWidget(self.btn)
        layout.addWidget(self.le)

        self.setEnterAction = QAction("Set Enter",self, shortcut=Qt.Key_Return)
        self.addAction(self.setEnterAction)

        self.btn1 = QPushButton("Please translate me!")
        self.btn1.setCheckable(True)
        self.btn1.toggle()
        self.btn1.setFont(font)
        self.btn1.setStyleSheet('color: white; background: green')
        self.btn1.resize(30,30)
        self.btn1.pressed.connect(self.translate)

        self.le1 = QTextEdit()
        self.le1.setFont(font)
        self.le1.setTabChangesFocus(True)
        # self.le2 = QTextEdit()
        # self.le2.setFont(font)
        # self.le2.setTabChangesFocus(True)
        layout.addWidget(self.btn1)
        layout.addWidget(self.le1)
        # layout.addWidget(self.le2)

        self.setLayout(layout)
        self.setWindowTitle("Translation")

    def language_selecting(self):
        if self.btn.isChecked():
            self.target = "de"
    
    def target_reset(self):
        self.target = "en"


    def translate(self):
        global PAPAGO_USER_ID, PAPAGO_USER_SECRET, text, result
        # text = self.le.text()
        text = self.le.toPlainText()
        self.le.clear()

        if text:
            # try:
                if self.target == "en":
                    ## Naver Papago translation for english
                    result = self.naver_trans("ko", self.target,text)
                    # result_en_de = self.google_trans("de",result)
                    # result_ko_de = self.naver_trans("ko","de",text)
                    self.le1.setText(str(result))
                    clipboard.copy(str(result))

                    # date = datetime.datetime.today()
                    # try:
                    #     last_day = int(time.ctime(os.path.getmtime('history.txt'))[8:10])
                    # except:
                    #     last_day = 0
                    
                    # try:
                    #     with open("history.txt", 'a') as history:
                    #         if last_day != date.day:
                    #             history.writelines('-------------- '+date.isoformat()+' ---------------'+'\n')
                    #         history.writelines('\n'+ text + '\n' + result + '\n' + result_en_de + '\n')
                    #         history.close()
                    # except OSError:
                    #     print('cannot open', history)

                elif self.target == "de":
                    ## Google translation for German
                    result = self.google_trans(self.target, text)
                    # result_naver = self.naver_trans("en",self.target,text)
                    self.le1.setText('src)\n'+str(text) +'\n'+'tgt)\n' +str(result))
                    # self.le2.setText(str(text)+'\n'+ str(result_naver))
                    clipboard.copy(str(text) + '\n' + str(result))
            # except:
            #     return self.le1.setText('Translation failed')

    def naver_trans(self,src,tgt,text):
        url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": PAPAGO_USER_ID, "X-Naver-Client-Secret":PAPAGO_USER_SECRET}
        params = {"source":src, "target":tgt, "text":text}
        response = requests.post(url, headers = headers, data=params)
        res = response.json()
        result = res['message']['result']['translatedText']
        return result

    def google_trans(self, tgt, text):
        translator = Translator()
        result = translator.translate(text, dest=tgt).text
        return result

class ConsoleTranslation():
    def __init__(self, src, tgt):
        self.src = src
        self.tgt = tgt
        self.text = input("input: ")

    def naver_trans(self):
        url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": PAPAGO_USER_ID, "X-Naver-Client-Secret": PAPAGO_USER_SECRET}
        params = {"source": self.src, "target": self.tgt, "text": self.text}
        response = requests.post(url, headers=headers, data=params)
        res = response.json()
        # f = open("res.json", 'w')
        # json.dump(res, f)
        try:
            output = res['message']['result']['translatedText']
        except:
            # If input is empty, the class should be reset.
            if not self.text:
                print('Select again the language pair')
            else:
            # Depending on the covered language pairs from API
                print("The selected langauge pair does not be served.")
            output = ""
        return output

    def translate(self):
        output = self.naver_trans()
        if output:
            print("output: {}".format(output))
            clipboard.copy(output)
        return output



# def main():
#     app = QApplication(sys.argv)
#     # win = QMainWindow()
#     ex = inputdialogdemo()
#     # ex.resize(w,h)
#     ex.show()
#     sys.exit(app.exec_())

def get

def main():
    while True:
        src = input("src: ") or "ko"
        tgt = input("tgt: ") or "en"
        while(1):
            output = ConsoleTranslation(src, tgt).translate()
            if not output:
                break


if __name__ == '__main__':
    main()

