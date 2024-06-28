import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QTabWidget()
        self.browser.setDocumentMode(True)
        self.browser.tabBarDoubleClicked.connect(self.open_new_tab)
        self.browser.currentChanged.connect(self.current_tab_changed)
        self.browser.setTabsClosable(True)
        self.browser.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.browser)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        self.add_navbar_buttons()

        self.setWindowTitle("Pedro Alvarez")
        self.showMaximized()

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

    def add_navbar_buttons(self):
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(lambda: self.browser.currentWidget().back())
        self.navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(lambda: self.browser.currentWidget().forward())
        self.navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(lambda: self.browser.currentWidget().reload())
        self.navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        stop_btn = QAction('Stop', self)
        stop_btn.triggered.connect(lambda: self.browser.currentWidget().stop())
        self.navbar.addAction(stop_btn)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.browser.addTab(browser, label)
        self.browser.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.browser.setTabText(i, browser.page().title()))

    def open_new_tab(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.browser.currentWidget().url()
        self.update_urlbar(qurl, self.browser.currentWidget())
        self.update_title(self.browser.currentWidget())

    def close_current_tab(self, i):
        if self.browser.count() < 2:
            return
        self.browser.removeTab(i)

    def navigate_home(self):
        self.browser.currentWidget().setUrl(QUrl('http://www.google.com'))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.browser.currentWidget():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def update_title(self, browser):
        if browser != self.browser.currentWidget():
            return
        title = self.browser.currentWidget().page().title()
        self.setWindowTitle("% s - Pedro Alvarez" % title)


app = QApplication(sys.argv)
QApplication.setApplicationName("Pedro Alvarez")
window = Browser()
app.exec_()
