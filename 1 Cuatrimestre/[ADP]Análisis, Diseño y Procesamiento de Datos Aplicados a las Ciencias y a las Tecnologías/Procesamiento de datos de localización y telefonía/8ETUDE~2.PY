from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Milan_CDR_db']
collection = db['Milan_CDR_c_cumules_par_heure']

# Identifiants des cellules à étudier
cellids = [4259, 4456, 5060, 1419, 2436, 4990, 945, 5048]

# Requête pour récupérer les données pour les cellules spécifiées
resultats = collection.find({"_id.Cellid": {"$in": cellids}})

# Affichage des résultats
for resultat in resultats:
    print(f"Cellid: {resultat['_id']['Cellid']}, Heure: {resultat['_id']['Heure']}")
    print(f"Total Smsin: {resultat.get('Total_Smsin', 0)}")
    print(f"Total Smsout: {resultat.get('Total_Smsout', 0)}")
    print(f"Total Callin: {resultat.get('Total_Callin', 0)}")
    print(f"Total Callout: {resultat.get('Total_Callout', 0)}")
    print(f"Total Internet: {resultat.get('Total_Internet', 0)}\n")
