from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np
import pandas as pd

# Simular la carga de datos. En tu caso, cargarías los datos de MongoDB.
# Por ahora, voy a crear un DataFrame de ejemplo con datos ficticios.
# Tu DataFrame debe ser creado basándote en tus datos reales de MongoDB.

# Crear un DataFrame de ejemplo
num_samples = 100  # Supongamos que tienes 100 compuestos
num_features = 1024  # Supongamos 1024 fingerprints

# Generar datos aleatorios
X = np.random.randint(2, size=(num_samples, num_features))
y = np.random.randint(2, size=(num_samples))

# Convertir a DataFrame y asignar clase
df = pd.DataFrame(X, columns=[f'FP{i+1}' for i in range(num_features)])
df['class'] = y

# Eliminar columnas donde todos los valores sean '0'
df = df.loc[:, (df != 0).any(axis=0)]

# Dividir los datos en entrenamiento y prueba
X = df.drop('class', axis=1)
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Crear y entrenar el modelo de clasificación
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = clf.predict(X_test)

# Calcular e imprimir métricas de rendimiento
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
print(f'Accuracy: {accuracy:.2f}')
print(f'ROC AUC: {roc_auc:.2f}')
