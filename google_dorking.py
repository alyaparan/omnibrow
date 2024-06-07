from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QWidget

class GoogleDorking:
    def __init__(self, browser):
        self.browser = browser
        self.dork_options_combo = QComboBox()
        self.dork_options_combo.addItems([
            "intitle", "inurl", "intext", "cache", "define", "link", "related", "info"
        ])
        self.dork_parameter_input = QLineEdit()

    def perform_google_dorking(self):
        selected_option = self.dork_options_combo.currentText()
        parameter = self.dork_parameter_input.text()

        dork_query = f"{selected_option}:{parameter}"

        dorking_url = QUrl(f"https://www.google.com/search?q={dork_query}")
        self.browser.setUrl(dorking_url)

    def get_widget(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Dork Query:"))
        layout.addWidget(self.dork_options_combo)
        layout.addWidget(QLabel("Enter Query Parameter:"))
        layout.addWidget(self.dork_parameter_input)
        perform_dorking_button = QPushButton("Perform Dorking")
        perform_dorking_button.clicked.connect(self.perform_google_dorking)
        layout.addWidget(perform_dorking_button)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
