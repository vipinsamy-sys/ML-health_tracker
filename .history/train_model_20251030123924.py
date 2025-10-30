# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# --- Step 1: Create sample dataset ---
# Replace this later with a real dataset
data = {
    'age': [25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
    'bmi': [18, 22, 25, 28, 30, 32, 34, 36, 38, 40],
    'glucose': [90, 95, 100, 110, 120, 130, 140, 150, 160, 170],
    'blood_pressure': [70, 75, 80, 82, 85, 88, 90, 92, 95, 98],
    'risk': [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]  # 0 = low risk, 1 = high risk
}
df = pd.DataFrame(data)

# --- Step 2: Split features and labels ---
X = df[['age', 'bmi', 'glucose', 'blood_pressure']]
y = df['risk']

# --- Step 3: Train-Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 4: Train Model ---
model = RandomForestClassifier()
model.fit(X_train, y_train)

# --- Step 5: Evaluate Model ---
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Model trained successfully with accuracy: {acc*100:.2f}%")

# --- Step 6: Save Model ---
joblib.dump(model, 'model.pkl')
print("💾 Model saved as 'model.pkl'")
