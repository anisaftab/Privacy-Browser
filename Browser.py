import sys
from turtle import forward
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtPrintSupport, QtWidgets

class TabBar(QTabBar):
        def tabSizeHint(self, index):
            size = QTabBar.tabSizeHint(self, index)
            w = 250
            return QSize(w, size.height())



class MainWindow( QMainWindow ):

    

    def __init__(self,  *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Privacy Browser")
        self.setWindowIcon(QIcon("icons/browser.png"))
        self.setGeometry(200,200,900,600)

        #Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

    
        #Back button
        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon("icons/back-arrow.png"))
        self.backButton.setIconSize(QSize(36,36))
        self.backButton.clicked.connect(self.backButtonAction)
        navbar.addWidget(self.backButton)
        
        #Forward button
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon("icons/forward-arrow.png"))
        self.forwardButton.setIconSize(QSize(36,36))
        self.forwardButton.clicked.connect(self.forwardButtonAction)
        navbar.addWidget(self.forwardButton)

        #Refresh button
        self.refreshButton = QPushButton()
        self.refreshButton.setIcon(QIcon("icons/refresh.png"))
        self.refreshButton.setIconSize(QSize(36,36))
        self.refreshButton.clicked.connect(self.refreshButtonAction)
        navbar.addWidget(self.refreshButton)

        #Home button
        self.homeButton = QPushButton()
        self.homeButton.setIcon(QIcon("icons/home.png"))
        self.homeButton.setIconSize(QSize(36,36))
        self.homeButton.clicked.connect(self.homeButtonAction)
        navbar.addWidget(self.homeButton)

        #AddressBar
        self.addressLine = QLineEdit()
        self.addressLine.setFont(QFont("Montserrat", 12))
        self.addressLine.setFixedHeight(40)
        self.addressLine.setMaxLength(75)
        self.addressLine.returnPressed.connect(self.searchButtonAction)
        navbar.addWidget(self.addressLine)


        #Search button
        self.searchButton = QPushButton()
        self.searchButton.setIcon(QIcon("icons/search.png"))
        self.searchButton.setIconSize(QSize(36,36))
        self.searchButton.clicked.connect(self.searchButtonAction)
        navbar.addWidget(self.searchButton)

        #Export to PDF button
        self.pdfButton = QPushButton()
        self.pdfButton.setIcon(QIcon("icons/pdf.png"))
        self.pdfButton.setIconSize(QSize(36,36))
        self.pdfButton.clicked.connect(self.exportToPDF)
        navbar.addWidget(self.pdfButton)

        #Quit button
        self.quitButton = QAction( "Quit", self)
        self.quitButton.setFont(QFont('Monteserrat',12))
        self.quitButton.triggered.connect(self.closeBrowser)

        #Add Tab from Menu
        self.addTabButton = QAction('New Tab',self)
        self.addTabButton.setFont(QFont('Monteserrat',12))
        self.addTabButton.triggered.connect(self.addNewTab)

        #Search Flights
        self.searchFlightsButton = QAction('Search Flights',self)
        self.searchFlightsButton.setFont(QFont('Monteserrat',12))
        self.searchFlightsButton.triggered.connect(self.searchFlights)
 
        #Menu
        menu = self.menuBar()
        fileMenu = menu.addMenu("&Menu")
        fileMenu.addAction(self.addTabButton)
        fileMenu.addAction(self.searchFlightsButton)
        fileMenu.addAction(self.quitButton)
        


        #Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabBar(TabBar())
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

        #New Tab button
        self.newTab = QPushButton('New Tab')
        self.newTab.setFont(QFont('Monteserrat',12))
        self.newTab.setIcon(QIcon("icons/new-tab.png"))
        self.newTab.setIconSize(QSize(36,36))
        self.tabs.setCornerWidget(self.newTab)
        self.newTab.clicked.connect(self.addNewTab)

        

        self.setCentralWidget(self.tabs)
        self.resize(1280, 720)
        self.addNewTab()
        self.show()


    
    def searchButtonAction(self):
        searchUrl = self.addressLine.text()
        self.tabs.currentWidget().load(QUrl(searchUrl))

    def backButtonAction(self):
        self.tabs.currentWidget().back()

    def forwardButtonAction(self):
        self.tabs.currentWidget().forward()

    def refreshButtonAction(self):
        self.tabs.currentWidget().reload()

    def homeButtonAction(self):
        self.tabs.currentWidget().load(QUrl('https://google.com'))

    def exportToPDF(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.editor.document().print_(dialog.printer())
        QMessageBox.information(self,'info','page exported')

    def closeBrowser(self):
        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
        self.close()

    def searchFlights(self):
        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()

        self.addNewTab('http://www.kayak.com')
        self.addNewTab('http://www.cheapoair.com')
        self.addNewTab('http://www.priceline.com')
        self.addNewTab('http://www.skyscanner.com')
        self.addNewTab('https://www.google.com/flights')


    def cookieFilter(request):
        print(
            f"firstPartyUrl: {request.firstPartyUrl.toString()}, origin: {request.origin.toString()}, thirdParty? {request.thirdParty}"
        )
        return False


    def addNewTab(self, arg = 'https://google.com' ):

        webEngineView = QWebEngineView()

        cookieStore = webEngineView.page().profile().cookieStore()
        cookieStore.deleteAllCookies()

        webEngineView.createWindow = self.addNewTab

        tabIndex = self.tabs.addTab(webEngineView, 'New Tab')

        webEngineView.urlChanged.connect(
            lambda x: self.tabs.setTabText(tabIndex, x.toString())
        )
        webEngineView.urlChanged.connect(
            lambda x: self.addressLine.setText(x.toString())
        )

       
        if(arg == False):
            webEngineView.load(QUrl('http://www.google.com'))
        else:
            webEngineView.load(QUrl(arg))

        
        
        

        return webEngineView
    


app = QApplication(sys.argv)
window = MainWindow()
window.show()
QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
sys.exit(app.exec_())



'''
Icons taken from:
"https://iconscout.com/icons/search" Search Icon "https://iconscout.com/contributors/latesticon"  Latest Icon 
"https://iconscout.com/icons/search" Search Icon "https://iconscout.com/contributors/google-inc" Google Inc. on "https://iconscout.com" - IconScout

'''