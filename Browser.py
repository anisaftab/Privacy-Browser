import sys
from turtle import forward
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

class MainWindow( QMainWindow ):

    def __init__(self,  *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Privacy Browser")
        self.setWindowIcon(QIcon("icons/browser.png"))
        

        self.browser = QWebEngineView()
        self.browser.setUrl( QUrl('http://google.com') )
        self.setCentralWidget( self.browser )
        self.showMaximized()

        #Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        #Back button
        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon("icons/back.png"))
        self.backButton.setIconSize(QSize(36,36))
        navbar.addWidget(self.backButton)
        
        #Forward button
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon("icons/forward.png"))
        self.forwardButton.setIconSize(QSize(36,36))
        navbar.addWidget(self.forwardButton)

        #Refresh button
        refresh_button = QAction('Reload Page', self)
        refresh_button.triggered.connect(self.browser.reload)
        refresh_button.setStatusTip('Reload this page')
        navbar.addAction(refresh_button)

        #Home button
        self.homeButton = QPushButton()
        self.homeButtonButton.setIcon(QIcon("icons/home.png"))
        self.backButton.setIconSize(QSize(36,36))
        navbar.addWidget(self.homeButton)

        #Stop loading button
        stop_button = QAction('Stop Loading', self)
        stop_button.triggered.connect(self.browser.stop)
        stop_button.setStatusTip('Stop loading this page')
        navbar.addAction(stop_button)
        self.show()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect( self.update_url )



    # function to take us back to home page
    def navigate_to_home(self):
        self.browser.setUrl( QUrl('http://google.com') )

    # function to take us to typed url
    def navigate_to_url(self):
        url = self.url_bar.text() 
        self.browser.setUrl(QUrl(url))

    # function to take us back to home page
    def update_url(self, previous_url):
        self.url_bar.setText(previous_url.toString())



app = QApplication(sys.argv)
QApplication.setApplicationName('No Tracking Browser')
window = MainWindow()
app.exec_()
