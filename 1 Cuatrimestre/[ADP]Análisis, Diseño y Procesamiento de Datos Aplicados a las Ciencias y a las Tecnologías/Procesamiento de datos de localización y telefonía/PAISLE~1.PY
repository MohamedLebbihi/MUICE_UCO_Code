from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)  # Assurez-vous que cela correspond à votre configuration MongoDB
db = client['Milan_CDR_db']  # Nom de la base de données
collection = db['Milan_CDR_c']  # Nom de la collection
# Compter les occurrences de la valeur 39 pour countrycode
occurrences_39 = collection.count_documents({"Countrycode": 39})
print(f"Nombre d'occurrences de la valeur 39 pour Countrycode: {occurrences_39}")
# Pipeline d'agrégation pour trouver le countrycode le plus répété (à l'exception de 39)
pipeline = [
    {"$match": {"Countrycode": {"$ne": 39}}},  # Exclure les documents où countrycode est 39
    {"$group": {"_id": "$Countrycode", "count": {"$sum": 1}}},  # Grouper par countrycode et compter
    {"$sort": {"count": -1}},  # Trier par count décroissant
    {"$limit": 1}  # Limiter à la valeur la plus répétée
]
# Exécuter l'agrégation
resultat = list(collection.aggregate(pipeline))
if resultat:
    # Afficher le countrycode le plus fréquent (à l'exception de 39) et son nombre d'occurrences
    print(f"Countrycode le plus répété (à l'exception de 39): {resultat[0]['_id']}, Nombre d'occurrences: {resultat[0]['count']}")
else:
    print("Aucun countrycode trouvé ou tous sont 39.")
