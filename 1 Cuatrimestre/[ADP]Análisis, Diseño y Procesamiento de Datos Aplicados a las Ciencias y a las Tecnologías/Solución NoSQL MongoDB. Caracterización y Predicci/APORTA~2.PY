from pymongo import MongoClient
from random import randint
import datetime

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Aportado']

# Collection Departments
departments = db['departments']
# Collection Employees
employees = db['employees']

# Créer 10 départements
for i in range(1, 11):
    department = {
        "DEPTNO": str(i),
        "DNAME": f"Departement_{i}",
        "LOC": f"Emplacement_{i}"
    }
    departments.insert_one(department)

# Créer 10 employés et les assigner à des départements aléatoires
for j in range(1, 11):
    employee = {
        "EMPNO": str(1000 + j),
        "ENAME": f"Employe_{j}",
        "JOB": f"Poste_{j}",
        "HIREDATE": datetime.datetime.now() - datetime.timedelta(days=randint(0, 3650)),
        "SAL": randint(30000, 60000),
        "DEPTNO": str(randint(1, 10))  # Assigner un numéro de département aléatoire
    }
   
    if j != 10:  
        employee['MANAGER'] = str(1000 + randint(1, 9))
    
    employees.insert_one(employee)

    # Trouver tous les employés d'un département
for employee in employees.find({"DEPTNO": "10"}):
    print(employee)

# Trouver le chef d'un employé donné
boss = employees.find_one({"EMPNO": "7934"})['MANAGER']
print(employees.find_one({"EMPNO": boss}))

# Agréger les salaires par département
pipeline = [
  {
    "$group": {
      "_id": "$DEPTNO",
      "total_salary": {"$sum": "$SAL"}
    }
  }
]
for result in employees.aggregate(pipeline):
    print(result)

