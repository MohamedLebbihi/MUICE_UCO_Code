from pymongo import MongoClient
# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Milan_CDR_db']
collection = db['Milan_CDR_c']
# Pipeline d'agrégation pour calculer les totaux accumulés par Cellid
pipeline = [
    {
        "$group": {
            "_id": "$Cellid",  # Groupement par Cellid
            "Total_Smsin": {"$sum": "$Smsin"},
            "Total_Smsout": {"$sum": "$Smsout"},
            "Total_Callin": {"$sum": "$Callin"},
            "Total_Callout": {"$sum": "$Callout"},
            "Total_Internet": {"$sum": "$Internet"}
        }
    }
]
# Exécution de l'agrégation
resultats = list(collection.aggregate(pipeline))
# Nom de la nouvelle collection pour les documents cumulés
nouvelle_collection = db['Milan_CDR_c_cumules']
# Insertion des documents cumulés dans la nouvelle collection
nouvelle_collection.insert_many(resultats)
