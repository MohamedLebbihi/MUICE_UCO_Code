from pymongo import MongoClient
import json
import os

# Chemin vers le dossier contenant les fichiers JSON
dossier_json = 'Milan_CDR/DossierJson'

# Connexion à MongoDB
client = MongoClient('localhost', 27017)  # Ajustez si nécessaire
db = client['Milan_CDR_db']  # Nom de la base de données
collection = db['Milan_CDR_c']  # Nom de la collection

# Itérer sur tous les fichiers JSON dans le dossier
for nom_fichier in os.listdir(dossier_json):
    chemin_complet = os.path.join(dossier_json, nom_fichier)
    if os.path.isfile(chemin_complet) and nom_fichier.endswith('.json'):
        with open(chemin_complet, 'r') as fichier:
            donnees = json.load(fichier)
            
            # Vérifier si 'donnees' est une liste de documents, sinon l'envelopper dans une liste
            if isinstance(donnees, dict):
                donnees = [donnees]
            
            # Insérer les données dans la collection MongoDB
            collection.insert_many(donnees)

print("Tous les fichiers JSON ont été chargés avec succès dans la collection 'Milan_CDR_c'.")
