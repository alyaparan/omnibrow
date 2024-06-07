from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTextEdit, QApplication
from bs4 import BeautifulSoup
import requests

class URLParser:
    def __init__(self, browser):
        self.browser = browser
        self.parsed_url_textedit = QTextEdit()
        self.parsed_url_textedit.setReadOnly(True)

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

    def copy_parsed_url(self):
        parsed_url_text = self.parsed_url_textedit.toPlainText()
        QApplication.clipboard().setText(parsed_url_text)

    def clear_parsed_url(self):
        self.parsed_url_textedit.clear()

    def get_widget(self):
        return self.parsed_url_textedit
