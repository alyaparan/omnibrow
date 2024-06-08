from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from bs4 import BeautifulSoup
import socket
import requests
import whois
import ssl
import OpenSSL
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setupBrowser()
        self.setupToolBar()
        self.setupOptionsDock()
        self.setWindowTitle("OmniBrow v1.0.2")
        self.show()

    def setupBrowser(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

    def setupToolBar(self):
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        actions = [("Back", self.browser.back), ("Forward", self.browser.forward),
                   ("Reload", self.browser.reload), ("Home", self.navigate_home)]
        for action_name, action_func in actions:
            action = QAction(action_name, self)
            action.setStatusTip(action_name)
            action.triggered.connect(action_func)
            navtb.addAction(action)
        navtb.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

    def setupOptionsDock(self):
        options_dock = QDockWidget("Options", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, options_dock)
        options_widget = QWidget()
        options_layout = QVBoxLayout()
        self.setupUrlParsing(options_layout)
        self.setupGoogleDorking(options_layout)
        self.setupDomainInformation(options_layout)
        options_widget.setLayout(options_layout)
        options_dock.setWidget(options_widget)

    def setupUrlParsing(self, layout):
        url_parsing_group = QGroupBox("URL Parsing")
        url_parsing_layout = QVBoxLayout()
        parse_url_button = QPushButton("Parse URL")
        parse_url_button.clicked.connect(self.parse_url)
        url_parsing_layout.addWidget(parse_url_button)
        self.parsed_url_textedit = QTextEdit()
        self.parsed_url_textedit.setReadOnly(True)
        url_parsing_layout.addWidget(self.parsed_url_textedit)
        url_parsing_group.setLayout(url_parsing_layout)
        layout.addWidget(url_parsing_group)

    def setupGoogleDorking(self, layout):
        google_dorking_group = QGroupBox("Google Dorking")
        google_dorking_layout = QVBoxLayout()
        self.dork_options_combo = QComboBox()
        self.dork_options_combo.addItems([
            "intitle", "inurl", "intext", "cache", "define", "link", "related", "info",
            "site", "filetype", "ext", "inanchor", "allintitle", "allinurl"
        ])
        google_dorking_layout.addWidget(QLabel("Select Dork Query:"))
        google_dorking_layout.addWidget(self.dork_options_combo)
        self.dork_parameter_input = QLineEdit()
        google_dorking_layout.addWidget(QLabel("Enter Query Parameter:"))
        google_dorking_layout.addWidget(self.dork_parameter_input)
        perform_dorking_button = QPushButton("Perform Dorking")
        perform_dorking_button.clicked.connect(self.perform_google_dorking)
        google_dorking_layout.addWidget(perform_dorking_button)
        google_dorking_group.setLayout(google_dorking_layout)
        layout.addWidget(google_dorking_group)

    def setupDomainInformation(self, layout):
        domain_group = QGroupBox("Domain Information")
        domain_layout = QVBoxLayout()
        domain_layout.addWidget(QLabel("Enter Domain:"))
        self.domain_input = QLineEdit()
        domain_layout.addWidget(self.domain_input)
        network_lookup_button = QPushButton("Network Lookup")
        network_lookup_button.clicked.connect(self.network_lookup)
        domain_layout.addWidget(network_lookup_button)
        self.domain_info_textedit = QTextEdit()
        self.domain_info_textedit.setReadOnly(True)
        domain_layout.addWidget(self.domain_info_textedit)
        domain_group.setLayout(domain_layout)
        layout.addWidget(domain_group)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s - OmniBrow v1.0.2" % title)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def parse_url(self):
        url = self.browser.url().toString()
        parsed_url = QUrl(url)
        parsed_url_text = f"Scheme: {parsed_url.scheme()}\n" \
                        f"Host: {parsed_url.host()}\n" \
                        f"Path: {parsed_url.path()}"
        if "google.com/search" in url:
            search_urls = self.extract_google_search_urls(url)
            parsed_url_text += "\n\n" + "\n".join(search_urls)
        self.parsed_url_textedit.setPlainText(parsed_url_text)

    def extract_google_search_urls(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            search_results = soup.find_all('a', href=True)
            urls = []
            for result in search_results:
                link = result['href']
                if link.startswith('/url?q='):
                    link = link.split('/url?q=')[1].split('&')[0]
                    urls.append(link)
            return urls
        except Exception as e:
            return ["Error occurred while extracting URLs:", str(e)]

    def perform_google_dorking(self):
        selected_option = self.dork_options_combo.currentText()
        parameter = self.dork_parameter_input.text()
        dork_query = f"{selected_option}:{parameter}"
        dorking_url = QUrl(f"https://www.google.com/search?q={dork_query}")
        self.browser.setUrl(dorking_url)

    def network_lookup(self):
        domain = self.domain_input.text()
        try:
            dns_result = socket.gethostbyname(domain)
            ip_info = requests.get(f"https://ipinfo.io/{dns_result}/json").json()
            ip_info_text = "\n".join([f"{k}: {v}" for k, v in ip_info.items()])
            whois_result = whois.whois(domain)
            whois_info_text = "\n".join([f"{k}: {v}" for k, v in whois_result.items()])
            cert = ssl.get_server_certificate((domain, 443))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            ssl_info_text = "\n".join([f"{x509.get_subject().CN}", f"Issuer: {x509.get_issuer().CN}"])

            result_text = (f"DNS Lookup result for {domain}:\n{dns_result}\n\n"
                        f"IP Lookup result for {domain}:\n{ip_info_text}\n\n"
                        f"WHOIS Lookup result for {domain}:\n{whois_info_text}\n\n"
                        f"SSL Certificate for {domain}:\n{ssl_info_text}")
            self.domain_info_textedit.setPlainText(result_text)
        except Exception as e:
            self.domain_info_textedit.setPlainText(f"Network Lookup failed:\n{e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
