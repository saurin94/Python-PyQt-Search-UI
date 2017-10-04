import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import QListWidgetItem, QStandardItem, QStandardItemModel, QLabel, QColor, QIcon, QVBoxLayout
from user_interface import Ui_MainWindow
from elasticsearch import Elasticsearch


class Main(QtGui.QMainWindow):

    def __init__(self):
        self.jsonDict = {}
        self.urlRate = {}
        self.url = ""
        self.title = ""
        self.cleanHTML = ""
        self.item = ""
        self.f = open("fileWrite.txt", "w")
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.search_button_clicked)
        self.ui.pushButton_2.clicked.connect(lambda: self.clicked(self.url, self.item, self.ui.pushButton_2))
        self.ui.pushButton_3.clicked.connect(lambda: self.clicked(self.url, self.item, self.ui.pushButton_3))
        self.ui.pushButton_4.clicked.connect(lambda: self.clicked(self.url, self.item, self.ui.pushButton_4))

    def search_button_clicked(self):
        urlsSet = set()
        t = self.ui.textEdit_3.toPlainText()
        name = self.ui.textEdit.toPlainText()
        es = Elasticsearch()
        query_phrase = str(t).lower()
        body_query = {
            "query": {
                "match": {
                    "text": query_phrase
                }
            },
            "size": 500
        }
        res = es.search(index="mi", doc_type="document", body=body_query, request_timeout=70)
        for i in res['hits']['hits']:
            url = i['_source']['docno'].encode("utf-8", "ignore").lower()
            self.jsonDict[url] = i['_source']
            if len(urlsSet) < 200:
                urlsSet.add(url)
            else:
                break
        for url in urlsSet:
            item = QListWidgetItem(url)
            self.ui.listWidget.addItem(item)
        item = self.ui.listWidget.currentItemChanged.connect(self.item_click)
        return item

    def item_click(self, item):
        self.url = str(item.text()).encode("utf-8", "ignore")
        self.title = "TITLE :\t" + self.jsonDict[self.url]['title'].encode("utf-8", "ignore")
        self.author = "AUTHOR : \t" + self.jsonDict[self.url]['author'].encode("utf-8", "ignore")
        self.cleanHTML = "ClEAN_TEXT : \n" + self.jsonDict[self.url]['text'].encode("utf-8", "ignore")
        self.ui.title.setText(self.title)
        self.ui.author.setText(self.author)
        self.ui.cleanHTML.setText(self.cleanHTML)
        self.ui.tabWidget.setCurrentIndex(1)
        self.item = item

    def clicked(self, url, item, button_id):
        print button_id.text()

        if button_id.text() == '0':
            self.f.write(url + ">>0" + "\n")
            self.ui.listWidget.item(self.ui.listWidget.row(item)).setIcon(QIcon(r"tick.png"))
            # self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
            # self.ui.listWidget.setItemSelected(self.ui.listWidget.row(item), self.ui.listWidget)
            self.ui.tabWidget.setCurrentIndex(0)

        elif button_id.text() == '1':
            self.f.write(url + ">>1" + "\n")
            self.ui.listWidget.item(self.ui.listWidget.row(item)).setIcon(QIcon(r"tick.png"))
            # self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
            self.ui.tabWidget.setCurrentIndex(0)

        elif button_id.text() == '2':
            self.f.write(url + ">>2" + "\n")
            # self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
            self.ui.listWidget.item(self.ui.listWidget.row(item)).setIcon(QIcon(r"tick.png"))
            self.ui.tabWidget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
