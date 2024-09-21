from pymongo import MongoClient
# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['Milan_CDR_db']
collection = db['Milan_CDR_c']
# Pipeline d'agrégation pour compter les valeurs non nulles et trouver le maximum dans chaque catégorie
pipeline = [
    {
        "$group": {
            "_id": "$Cellid",
            "Smsin_Count": {"$sum": {"$cond": [{"$ne": ["$Smsin", 0]}, 1, 0] }},       
            "Smsout_Count": {"$sum": {"$cond": [{"$ne": ["$Smsout", 0]}, 1, 0] } },
            "Callin_Count": {"$sum": {   "$cond": [{"$ne": ["$Callin", 0]}, 1, 0] } },
            "Callout_Count": { "$sum": {"$cond": [{"$ne": ["$Callout", 0]}, 1, 0]    } }, 
            "Internet_Count": { "$sum": {  "$cond": [{"$ne": ["$Internet", 0]}, 1, 0]         }   }       
        }
    },
    #je montre comment récupérer la valeur la plus élevée de toutes les catégories.
    {
        "$project": {
            "Cellid": "$_id",
            "Smsin_Count": 1,
            "Smsout_Count": 1,
            "Callin_Count": 1,
            "Callout_Count": 1,
            "Internet_Count": 1,
            "Total_Count": { "$add": [ "$Smsin_Count", "$Smsout_Count", "$Callin_Count", "$Callout_Count", "$Internet_Count" ] }
        }
    },
    { "$sort": { "Total_Count": -1 } },
    { "$limit": 1 }
]
# Exécuter l'agrégation
resultat = list(collection.aggregate(pipeline))
# Affichage du résultat
if resultat:
    print(f"Cellid avec le plus d'activité non-nulle: {resultat[0]['Cellid']}")
    print(f"Smsin non-zero count: {resultat[0]['Smsin_Count']}")
    print(f"Smsout non-zero count: {resultat[0]['Smsout_Count']}")
    print(f"Callin non-zero count: {resultat[0]['Callin_Count']}")
    print(f"Callout non-zero count: {resultat[0]['Callout_Count']}")
    print(f"Internet non-zero count: {resultat[0]['Internet_Count']}")
    print(f"Total non-zero count: {resultat[0]['Total_Count']}")
else:
    print("Aucun résultat trouvé.")
