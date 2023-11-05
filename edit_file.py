import binascii
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel
from file_manager import FileManager

#Classe qui gére l'édition de fichier
class FileEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenêtre principale
        self.setWindowTitle("Hexadecimal File Editor and Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Zone de texte du chemin du fichier
        self.file_path_input = QTextEdit(self)
        self.layout.addWidget(self.file_path_input)
        self.file_path_input.setReadOnly(True)
        self.file_path_input.setMaximumHeight(30)

        # Bouton pour choisir le fichier à ouvrir
        self.open_file_button = QPushButton("Open File", self)
        self.open_file_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_file_button)

        # Zone de texte du contenue Hexadécimal
        self.hex_label = QLabel("Contenu Hexadécimal :")
        self.hex_view = QTextEdit(self)
        self.layout.addWidget(self.hex_label)
        self.layout.addWidget(self.hex_view)

        # Bouton pour enregistrer le contenu hexadécimal dans le fichier
        self.save_button_hex = QPushButton("Enregistrer le contenu hexadécimal dans le fichier", self)
        self.save_button_hex.clicked.connect(self.save_file_hex)
        self.layout.addWidget(self.save_button_hex)

        # Zone de texte du contenue UTF-8
        self.ascii_label = QLabel("Contenu UTF-8 :")
        self.ascii_view = QTextEdit(self)
        self.ascii_view.setReadOnly(False)
        self.layout.addWidget(self.ascii_label)
        self.layout.addWidget(self.ascii_view)

        # Bouton pour enregistrer le contenu utf-8 dans le fichier
        self.save_button = QPushButton("Enregistrer le contenu utf-8 dans le fichier", self)
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.save_button)

        # Zone Information du fichier
        self.file_info_label = QLabel("", self)
        self.layout.addWidget(self.file_info_label)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Initialisation gestionnaire de fichier
        self.file_manager = FileManager()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_path:
            self.file_path_input.setPlainText(file_path)
            self.load_file(file_path)

    def load_file(self, file_path):
        hex_content, ascii_content = self.file_manager.read_file(file_path)
        self.hex_view.setPlainText(hex_content)
        self.ascii_view.setPlainText(ascii_content)
        file_info = self.file_manager.get_file_info(file_path)
        self.file_info_label.setText(file_info)

    #Permet la sauvegarde du fichier selon le contenu Hexadécimal
    def save_file_hex(self):
        file_path = self.file_path_input.toPlainText()
        hex_content = self.hex_view.toPlainText()
        self.file_manager.save_file(file_path, hex_content)
        self.load_file(file_path) #Mise à jour de l'apercu après les modifications

    #Permet la sauvegarde du fichier selon le contenu UTF-8
    def save_file(self):
        file_path = self.file_path_input.toPlainText()
        hex_content = binascii.hexlify(self.ascii_view.toPlainText().encode("utf-8")).decode('utf-8')
        self.file_manager.save_file(file_path, hex_content)
        self.load_file(file_path) #Mise à jour de l'apercu après les modifications
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileEditorWindow()
    window.show()
    sys.exit(app.exec_())
