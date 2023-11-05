import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

#Importation des différentes fenêtre d'édition
from edit_http import HttpEditorWindow
from edit_file import FileEditorWindow
from edit_image import ImageEditorWindow

#Classe de départ pour la navigation
class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Fenêtre principale
        self.setWindowTitle("Fenêtre Principale")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Bouton pour l'édition d'image
        image_button = QPushButton("Éditer une image")
        image_button.clicked.connect(self.open_image_editor)
        layout.addWidget(image_button)

        # Bouton pour l'édition de fichier
        file_button = QPushButton("Éditer un fichier")
        file_button.clicked.connect(self.open_file_editor)
        layout.addWidget(file_button)

        # Bouton pour le visionneur HTTP
        http_button = QPushButton("Visionner HTTP")
        http_button.clicked.connect(self.open_http_editor)
        layout.addWidget(http_button)

        central_widget.setLayout(layout)
        self.http_editor_window = None
        self.file_editor_window = None
        self.image_editor_window = None

    #Méthode d'ouverture des autres fenêtres
    def open_image_editor(self):
       if self.image_editor_window is None or not self.image_editor_window.isVisible():
            self.image_editor_window = ImageEditorWindow()
            self.image_editor_window.setWindowTitle("Éditeur Image")
            self.image_editor_window.show()

    def open_file_editor(self):
       if self.file_editor_window is None or not self.file_editor_window.isVisible():
            self.file_editor_window = FileEditorWindow()
            self.file_editor_window.setWindowTitle("Éditeur File")
            self.file_editor_window.show()

    def open_http_editor(self):
       if self.http_editor_window is None or not self.http_editor_window.isVisible():
            self.http_editor_window = HttpEditorWindow()
            self.http_editor_window.setWindowTitle("Éditeur HTTP")
            self.http_editor_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InitialWindow()
    window.show()
    sys.exit(app.exec_())
