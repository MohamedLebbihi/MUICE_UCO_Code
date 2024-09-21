from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)  # Assurez-vous que cela correspond à votre configuration MongoDB
db = client['Milan_CDR_db']  # Nom de la base de données
collection = db['Milan_CDR_c']  # Nom de la collection

# Récupérer les valeurs uniques de 'countrycode'
countrycodes_uniques = collection.distinct('Countrycode')

# Afficher les valeurs uniques de 'countrycode'
for countrycode in countrycodes_uniques:
    print(countrycode)
