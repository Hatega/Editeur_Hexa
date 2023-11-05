import sys
import PySide6
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel
from PySide6.QtCore import QSize
from image_manager import ImageManager
from PIL import Image
from PIL.ImageQt import ImageQt
import json

# Classe qui gère l'édition des images
class ImageEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenêtre principale de la page
        self.setWindowTitle("Hexadecimal Image Editor and Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Zone de texte chemin du fichier
        self.image_path_input = QTextEdit(self)
        self.layout.addWidget(self.image_path_input)
        self.image_path_input.setReadOnly(True)
        self.image_path_input.setMaximumHeight(30)

        # Bouton pour aller chercher le fichier Image à ouvrir
        self.open_image_button = QPushButton("Open Image", self)
        self.open_image_button.clicked.connect(self.open_image)
        self.layout.addWidget(self.open_image_button)

        # Zone de l'image
        self.image_label = QLabel("Image :")
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)

        # Zone de texte Hexadécimal
        self.hex_label = QLabel("Contenu Hexadécimal :")
        self.hex_view = QTextEdit(self)
        self.layout.addWidget(self.hex_label)
        self.layout.addWidget(self.hex_view)

        # Bouton pour enregistrer la partie Hexadécimal dans le fichier
        self.save_button = QPushButton("Enregistrer le contenu hexadécimal dans le fichier", self)
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.save_button)

        # Zone Information fichier
        self.file_info_label = QLabel("", self)
        self.layout.addWidget(self.file_info_label)

        # Zone d'affichage des données EXIF
        self.exif_label = QLabel("Données EXIF :")
        self.exif_view = QTextEdit(self)
        self.exif_view.setReadOnly(True)
        self.layout.addWidget(self.exif_label)
        self.layout.addWidget(self.exif_view)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Initialisation gestionnaire de fichier Image
        self.file_manager = ImageManager()

    def open_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if image_path:
            self.image_path_input.setPlainText(image_path)
            self.load_image(image_path)

    def load_image(self, image_path):
        with Image.open(image_path) as img:
            # Affichage de l'image
            qimage = ImageQt(img)
            pixmap = PySide6.QtGui.QPixmap.fromImage(qimage)
            pixmap_dim = pixmap.scaled(QSize(400, 400))
            self.image_label.setPixmap(pixmap_dim)

            # Affichage du contenu Hexa
            hex_content = self.file_manager.read_image_as_hex(image_path)
            self.hex_view.setPlainText(hex_content)
            width, height = img.size

            # Affichage des informations
            file_info = self.file_manager.get_file_info(image_path)
            self.file_info_label.setText(f"Taille : {width}x{height} | " + file_info)

            # Affichage des données EXIF
            exif_data = self.get_exif_data(img)
            self.exif_view.setPlainText(exif_data)

    def save_file(self):
        image_path = self.image_path_input.toPlainText()
        hex_content = self.hex_view.toPlainText()
        self.file_manager.save_image(image_path, hex_content)
        self.load_image(image_path)

    def get_exif_data(self, image):
        try:
            exif = image._getexif()  # Obtenir les données EXIF de l'image
            if exif:
                exif_dict = {
                    Image.TAGS[key]: exif[key]
                    for key in exif
                    if key in Image.TAGS
                }
                exif_json = json.dumps(exif_dict, indent=4, ensure_ascii=False)
                return exif_json
            else:
                return "Aucune donnée EXIF disponible pour cette image."
        except Exception as e:
            return f"Erreur lors de la récupération des données EXIF : {e}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditorWindow()
    window.show()
    sys.exit(app.exec_())
