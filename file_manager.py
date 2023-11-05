import binascii
from datetime import datetime
import os

#Classe qui gère les fichiers 
class FileManager:
    
    #Lecture d'un fichier au format Hexa et UTF-8
    def read_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read() #lecture binaire
                hex_content = binascii.hexlify(file_content).decode('utf-8') #conversion hexa
                ascii_content = file_content.decode('utf-8', errors='ignore') #conversion UTF-8
                return hex_content, ascii_content
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}") #gestion d'erreur - afficher dans la console
            return "", ""

    #Enregistrement du fichier à partir d'un contenu hexa
    def save_file(self, file_path, hex_content):
        try:
            binary_content = binascii.unhexlify(hex_content)
            with open(file_path, 'wb') as file:
                file.write(binary_content)
                print("Fichier enregistré avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du fichier : {e}") #gestion d'erreur - afficher dans la console

    #Information du fichier image
    def get_file_info(self, file_path):
        try:
            file_info = os.stat(file_path)
            file_size = file_info.st_size
            file_modified = file_info.st_mtime #temps dernière modif
            file_created = file_info.st_ctime #temps de création
            return f"Taille : {file_size} octets, Modifié : {datetime.fromtimestamp(file_modified)}, Créé : {datetime.fromtimestamp(file_created)}"
        except Exception as e:
            return "Informations sur le fichier non disponibles"
