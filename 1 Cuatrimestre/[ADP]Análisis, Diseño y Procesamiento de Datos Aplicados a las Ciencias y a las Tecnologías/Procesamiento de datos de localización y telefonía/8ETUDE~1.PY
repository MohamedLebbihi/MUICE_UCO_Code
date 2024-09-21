from pymongo import MongoClient
# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Milan_CDR_db']
collection = db['Milan_CDR_c']
# Identifiants des cellules à étudier
cellids = [4259, 4456, 5060, 1419, 2436, 4990, 945, 5048]
# Pipeline d'agrégation pour calculer les totaux par Cellid spécifié
pipeline = [
    {"$match": {"Cellid": {"$in": cellids}}},
    {"$group": {
        "_id": "$Cellid",
        "Total_Smsin": {"$sum": "$Smsin"},
        "Total_Smsout": {"$sum": "$Smsout"},
        "Total_Callin": {"$sum": "$Callin"},
        "Total_Callout": {"$sum": "$Callout"},
        "Total_Internet": {"$sum": "$Internet"}
    }}]
# Exécution de l'agrégation
resultats = list(collection.aggregate(pipeline))
# Affichage des résultats
for resultat in resultats:
    print(f"Cellid: {resultat['_id']}")
    print(f"Total Smsin: {resultat['Total_Smsin']}")
    print(f"Total Smsout: {resultat['Total_Smsout']}")
    print(f"Total Callin: {resultat['Total_Callin']}")
    print(f"Total Callout: {resultat['Total_Callout']}")
    print(f"Total Internet: {resultat['Total_Internet']}\n")
