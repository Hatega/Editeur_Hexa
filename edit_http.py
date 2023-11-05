import sys
import time
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import binascii

#Classe pour le visionneur HTTP
class HttpEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Fenêtre principal
        self.setGeometry(100, 100, 600, 500)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        #Zone de saisie URL
        self.url_label = QLabel("URL :")
        self.url_input = QLineEdit()
        self.url_input.setText("https://www.google.fr/")
        self.send_button = QPushButton("Send Request")

        #Zone du contenu Hexadécimal et UTF-8
        self.hexa_label = QLabel("Hexadécimal:")
        self.hexa_text = QTextEdit()
        self.ascii_label = QLabel("Réponse:")
        self.ascii_text = QTextEdit()

        #Zone d'info sur la requête HTTP
        self.info_label = QLabel("Info:")
        self.info_text = QTextEdit()

        #Zone de l'entête HTTP
        self.header_table = QTableWidget()
        self.header_table.setColumnCount(2)
        self.header_table.setHorizontalHeaderLabels(["Header", "Value"])
        self.header_table.setColumnWidth(0, 150)
        self.header_table.setColumnWidth(1, 300)

        #Mise en place du plan
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.ascii_label)
        layout.addWidget(self.ascii_text)
        layout.addWidget(self.hexa_label)
        layout.addWidget(self.hexa_text)
        layout.addWidget(self.info_label)
        layout.addWidget(self.info_text)
        layout.addWidget(self.header_table)

        #Bouton de fermeture de la fen^tre
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        central_widget.setLayout(layout)

        self.send_button.clicked.connect(self.send_request)

        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_response)


        self.hexa_text.cursorPositionChanged.connect(self.sync_cursor_position)

    #Mets le curseur de la zone ascii au même endroit que celui de la zone hexa
    def sync_cursor_position(self):
        hexa_cursor = self.hexa_text.textCursor()
        hexa_position = hexa_cursor.position()

        ascii_position = hexa_position // 2

        ascii_cursor = QTextCursor(self.ascii_text.document())
        ascii_cursor.setPosition(ascii_position)

        self.ascii_text.setTextCursor(ascii_cursor)



    def handle_response(self, reply):
        elapsed_time = time.time() - self.start_time
        self.send_button.setEnabled(True)
        self.info_text.append(f"Response Time: {elapsed_time:.2f} seconds")
        if reply.error() == QNetworkReply.NoError:
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            self.info_text.append(f"HTTP Status Code: {status_code}")

            content = reply.readAll().data()
            self.hexa_text.setPlainText(binascii.hexlify(content).decode("utf-8"))
            self.ascii_text.setPlainText(content.decode("utf-8"))

            headers = reply.rawHeaderList()

            for header in headers:
                header_cell = QTableWidgetItem(header.data().decode("utf-8"))
                value_cell = QTableWidgetItem(reply.rawHeader(header).data().decode("utf-8"))

                self.header_table.insertRow(self.header_table.rowCount())
                self.header_table.setItem(self.header_table.rowCount() - 1, 0, header_cell)
                self.header_table.setItem(self.header_table.rowCount() - 1, 1, value_cell)

        else:
            self.info_text.append("Error: " + reply.errorString())

    def send_request(self):
        url = self.url_input.text()
        if url:
            self.send_button.setEnabled(False)
            self.info_text.clear()
            self.header_table.setRowCount(0)
            self.hexa_text.clear()
            self.ascii_text.clear()
            self.start_time = time.time()
            request = QNetworkRequest(QUrl(url))
            self.network_manager.get(request)
