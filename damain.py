from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):

    def go_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))
    
    def update_url(self, url):
        self.url_bar.setText(url.toString())

    def go_home(self):
        self.browser.setUrl(QUrl('https://google.com'))

    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()
    
    def add_navbar_buttons(self):
        #tool bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        #back button
        back_btn = QAction('<-', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        #forward button
        forward_btn = QAction('->', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        #refresh button
        refresh_btn = QAction('refresh',self)
        refresh_btn.triggered.connect(self.browser.reload)
        navbar.addAction(refresh_btn)

        #home button
        home_btn = QAction('home',self)
        home_btn.triggered.connect(self.go_home)
        navbar.addAction(home_btn)

        #search bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.go_url)
        navbar.addWidget(self.url_bar)
        self.browser.urlChanged.connect(self.update_url)

        #stop
        stop_btn = QAction('Stop', self)
        stop_btn.triggered.connect(lambda: self.browser.currentWidget().stop())
        navbar.addAction(stop_btn)

app = QApplication(sys.argv)
QApplication.setApplicationName('Pedro Alvares teste 1')
windows = MainWindow()

app.exec()