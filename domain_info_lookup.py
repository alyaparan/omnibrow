import socket
import whois
import ssl
import OpenSSL
import requests
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel

class DomainInfoLookup:
    def __init__(self):
        self.domain_input = QLineEdit()
        self.domain_info_textedit = QTextEdit()
        self.domain_info_textedit.setReadOnly(True)

    def dns_lookup(self):
        domain = self.domain_input.text()
        try:
            result = socket.gethostbyname(domain)
            self.domain_info_textedit.setPlainText(f"DNS Lookup result for {domain}:\n{result}")
        except Exception as e:
            self.domain_info_textedit.setPlainText(f"DNS Lookup failed:\n{e}")

    def ip_lookup(self):
        domain = self.domain_input.text()
        try:
            result = socket.gethostbyname(domain)
            ip_info = requests.get(f"https://ipinfo.io/{result}/json").json()
            ip_info_text = "\n".join([f"{k}: {v}" for k, v in ip_info.items()])
            self.domain_info_textedit.setPlainText(f"IP Lookup result for {domain}:\n{ip_info_text}")
        except Exception as e:
            self.domain_info_textedit.setPlainText(f"IP Lookup failed:\n{e}")

    def whois_lookup(self):
        domain = self.domain_input.text()
        try:
            w = whois.whois(domain)
            whois_info_text = "\n".join([f"{k}: {v}" for k, v in w.items()])
            self.domain_info_textedit.setPlainText(f"WHOIS Lookup result for {domain}:\n{whois_info_text}")
        except Exception as e:
            self.domain_info_textedit.setPlainText(f"WHOIS Lookup failed:\n{e}")

    def sslcert_lookup(self):
        domain = self.domain_input.text()
        try:
            cert = ssl.get_server_certificate((domain, 443))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            ssl_info_text = "\n".join([f"{x509.get_subject().CN}", f"Issuer: {x509.get_issuer().CN}"])
            self.domain_info_textedit.setPlainText(f"SSL Certificate for {domain}:\n{ssl_info_text}")
        except Exception as e:
            self.domain_info_textedit.setPlainText(f"SSL Certificate Lookup failed:\n{e}")

    def get_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Domain:"))
        layout.addWidget(self.domain_input)
        
        dns_lookup_button = QPushButton("DNS Lookup")
        dns_lookup_button.clicked.connect(self.dns_lookup)
        layout.addWidget(dns_lookup_button)

        ip_lookup_button = QPushButton("IP Lookup")
        ip_lookup_button.clicked.connect(self.ip_lookup)
        layout.addWidget(ip_lookup_button)

        whois_lookup_button = QPushButton("WHOIS Lookup")
        whois_lookup_button.clicked.connect(self.whois_lookup)
        layout.addWidget(whois_lookup_button)

        sslcert_lookup_button = QPushButton("SSL Certificate Lookup")
        sslcert_lookup_button.clicked.connect(self.sslcert_lookup)
        layout.addWidget(sslcert_lookup_button)

        layout.addWidget(self.domain_info_textedit)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
