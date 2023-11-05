import binascii
import datetime
import os
from PIL import Image

#Classe qui gère les fichiers images
class ImageManager:

    #Lecture d'une image au format Hexa
    def read_image_as_hex(self, image_path):
        try:
            with open(image_path, 'rb') as file:
                image_data = file.read() #lecture binaire
                hex_content = binascii.hexlify(image_data).decode('utf-8') #conversion hexa
                return hex_content
        except Exception as e:
            print(f"Erreur lors de la lecture de l'image en format hexadécimal : {e}") #gestion erreur - afficher dans la console
            return ""

    #Enregistrement de l'image à partir de l'hexa
    def save_image(self, image_path, hex_content):
        try:
            binary_content = binascii.unhexlify(hex_content) #conversion binaire
            with open(image_path, 'wb') as file:
                file.write(binary_content) #écriture binaire
                print("Image enregistrée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'image : {e}") #gestion erreur - afficher dans la console

    #Information du fichier image
    def get_file_info(self, file_path):
        try:
            file_info = os.stat(file_path)
            file_size = file_info.st_size
            file_modified = file_info.st_mtime
            file_created = file_info.st_ctime
            return f"Taille : {file_size} octets, Modifié : {datetime.fromtimestamp(file_modified)}, Créé : {datetime.fromtimestamp(file_created)}"
        except Exception as e:
            return "Informations sur le fichier non disponibles"
