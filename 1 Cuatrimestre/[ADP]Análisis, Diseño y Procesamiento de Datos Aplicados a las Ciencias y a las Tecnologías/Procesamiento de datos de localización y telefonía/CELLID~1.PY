from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Milan_CDR_db']
collection = db['Milan_CDR_c']

# Pipeline d'agrégation pour trouver le 'cellid' le plus fréquent sans prendre en compte countrycode = 39
pipeline = [
    {"$match": {"Countrycode": {"$ne": 39}}},  # Exclure les documents où countrycode est 39
    {"$group": {"_id": "$Cellid", "count": {"$sum": 1}}},  # Grouper par 'cellid' et compter
    {"$sort": {"count": -1}},  # Trier par le nombre d'occurrences en ordre décroissant
    {"$limit": 1}  # Prendre le 'cellid' le plus fréquent
]

# Exécuter l'agrégation
resultat = list(collection.aggregate(pipeline))

if resultat:
    print(f"La Cellid qui communique le plus avec l'etranger: {resultat[0]['_id']}, Nombre d'occurrences: {resultat[0]['count']}")
else:
    print("Aucun Cellid trouvé ou tous ont un Countrycode de 39.")
