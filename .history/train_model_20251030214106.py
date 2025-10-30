import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

print("Starting model training...")

# Create dummy data
np.random.seed(42)
data = pd.DataFrame({
    'age': np.random.randint(20, 70, 100),
    'bmi': np.random.uniform(18, 35, 100),
    'bp': np.random.randint(80, 160, 100),
    'glucose': np.random.randint(70, 200, 100),
    'risk': np.random.randint(0, 2, 100)
})

print(" Dataset created successfully")

X = data[['age', 'bmi', 'bp', 'glucose']]
y = data['risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f" Model trained successfully with accuracy: {acc*100:.2f}%")

os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/model.pkl')
print(" Model saved as 'model/model.pkl'")
