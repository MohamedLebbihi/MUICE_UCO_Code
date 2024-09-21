from pymongo import MongoClient
# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Milan_CDR_db']
collection = db['Milan_CDR_c']
# Pipeline d'agrégation pour calculer les totaux accumulés par Cellid et heure extrait de timestamp
pipeline = [
    {
        "$addFields": {
            "Heure": {"$hour": "$timestamp"}  # Ajoute un champ Heure en extrayant l'heure du champ timestamp
        }
    },
    {
        "$group": {
            "_id": {
                "Cellid": "$Cellid",
                "Heure": "$Heure"  # Groupe par Cellid et Heure
            },
            "Total_Smsin": {"$sum": "$Smsin"},
            "Total_Smsout": {"$sum": "$Smsout"},
            "Total_Callin": {"$sum": "$Callin"},
            "Total_Callout": {"$sum": "$Callout"},
            "Total_Internet": {"$sum": "$Internet"}
        }}]
# Exécution de l'agrégation
resultats = list(collection.aggregate(pipeline))
# Nom de la nouvelle collection pour les documents cumulés par Cellid et heure
nouvelle_collection = db['Milan_CDR_c_cumules_par_heure']
# Insertion des documents cumulés dans la nouvelle collection
nouvelle_collection.insert_many(resultats)
