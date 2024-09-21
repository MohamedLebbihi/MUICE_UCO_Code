import json

# Liste des chemins vers vos fichiers .txt
fichiers_txt = [
    'C:/Users/Lebbihi Mohamed/Desktop/Milan/Milan_CDR/sms-call-internet-mi-2013-11-01.txt',
    'C:/Users/Lebbihi Mohamed/Desktop/Milan/Milan_CDR/sms-call-internet-mi-2013-11-02.txt',
    'C:/Users/Lebbihi Mohamed/Desktop/Milan/Milan_CDR/sms-call-internet-mi-2013-11-03.txt',
    'C:/Users/Lebbihi Mohamed/Desktop/Milan/Milan_CDR/sms-call-internet-mi-2013-11-04.txt',
    'C:/Users/Lebbihi Mohamed/Desktop/Milan/Milan_CDR/sms-call-internet-mi-2013-11-05.txt',
    'C:/Users/Lebbihi Mohamed/Desktop/Milan/Milan_CDR/sms-call-internet-mi-2013-11-06.txt',
    'C:/Users/Lebbihi Mohamed/Desktop/Milan/Milan_CDR/sms-call-internet-mi-2013-11-07.txt',
]

noms_colonnes = ["Cellid", "Time", "Countrycode", "Smsin", "Smsout", "Callin", "Callout", "Internet"]

for chemin_fichier in fichiers_txt:
    donnees_json = []
    with open(chemin_fichier, 'r') as fichier:
        for ligne in fichier:
            valeurs = ligne.strip().split()  # Ajustez si votre délimiteur n'est pas un espace
            valeurs += [0] * (8 - len(valeurs))  # Ajoute des zéros pour les valeurs manquantes
            valeurs = [float(valeur) for valeur in valeurs]  # Convertit en float
            
            ligne_dict = {noms_colonnes[i]: valeurs[i] for i in range(8)}
            donnees_json.append(ligne_dict)
    
    # Construire le nom du fichier JSON basé sur le nom du fichier TXT
    chemin_fichier_json = chemin_fichier.replace('.txt', '.json')
    
    # Sauvegarder les données dans un fichier JSON
    with open(chemin_fichier_json, 'w') as fichier_json:
        json.dump(donnees_json, fichier_json, indent=4)
