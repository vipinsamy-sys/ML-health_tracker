import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib
import os

print("🚀 Starting model training...")

# Define feature spaces
categorical_features = [
    'gender',
    'body_type',
    'diet_type',
    'physical_activity',
    'family_history',
    'stress_level',
    'smoking',
    'alcohol',
    'junk_food_freq',
]

numeric_features = [
    'age',
    'sleep_hours',
    'water_intake_liters',
]

# Create synthetic dataset with correlations to risk
np.random.seed(42)
N = 600
age = np.random.randint(18, 80, N)
gender = np.random.choice(['Male', 'Female', 'Other'], N, p=[0.49, 0.49, 0.02])
body_type = np.random.choice(['Slim', 'Average', 'Overweight'], N, p=[0.25, 0.5, 0.25])
diet_type = np.random.choice(['Vegetarian', 'Mixed', 'Fast-food lover'], N, p=[0.3, 0.5, 0.2])
physical_activity = np.random.choice(['Rarely', 'Sometimes', 'Regularly'], N, p=[0.25, 0.5, 0.25])
sleep_hours = np.clip(np.random.normal(6.8, 1.2, N), 3.5, 10.0)
smoking = np.random.choice(['Yes', 'No'], N, p=[0.2, 0.8])
alcohol = np.random.choice(['Yes', 'No'], N, p=[0.35, 0.65])
family_history = np.random.choice(['None', 'Diabetes', 'Heart Issues'], N, p=[0.55, 0.25, 0.2])
stress_level = np.random.choice(['Low', 'Medium', 'High'], N, p=[0.35, 0.45, 0.2])
water_intake_liters = np.clip(np.random.normal(2.4, 0.9, N), 0.8, 5.5)
junk_food_freq = np.random.choice(['Rarely', 'Weekly', 'Daily'], N, p=[0.45, 0.4, 0.15])

data = pd.DataFrame({
    'age': age,
    'gender': gender,
    'body_type': body_type,
    'diet_type': diet_type,
    'physical_activity': physical_activity,
    'sleep_hours': np.round(sleep_hours, 1),
    'smoking': smoking,
    'alcohol': alcohol,
    'family_history': family_history,
    'stress_level': stress_level,
    'water_intake_liters': np.round(water_intake_liters, 1),
    'junk_food_freq': junk_food_freq,
})

# Create a synthetic risk score influenced by factors
risk_score = (
    (age > 50).astype(int) * 0.7 +
    (body_type == 'Overweight').astype(int) * 0.9 +
    (diet_type == 'Fast-food lover').astype(int) * 0.8 +
    (physical_activity == 'Rarely').astype(int) * 0.8 +
    (sleep_hours < 6).astype(int) * 0.6 +
    (smoking == 'Yes').astype(int) * 0.8 +
    (alcohol == 'Yes').astype(int) * 0.3 +
    (family_history != 'None').astype(int) * 0.8 +
    (stress_level == 'High').astype(int) * 0.7 +
    (water_intake_liters < 2).astype(int) * 0.4 +
    (junk_food_freq == 'Daily').astype(int) * 0.7
)

# Convert continuous score to binary with noise
noise = np.random.normal(0, 0.4, N)
prob = 1 / (1 + np.exp(-(risk_score + noise - 1.6)))
risk = (np.random.rand(N) < prob).astype(int)

data['risk'] = risk

print("✅ Dataset with extended features created successfully")

X = data[categorical_features + numeric_features]
y = data['risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numeric_features),
    ]
)

clf = Pipeline(steps=[
    ('prep', preprocessor),
    ('model', LogisticRegression(max_iter=1000))
])

clf.fit(X_train, y_train)

pred = clf.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"🎯 Model trained successfully with accuracy: {acc*100:.2f}%")

os.makedirs('model', exist_ok=True)
joblib.dump({'pipeline': clf, 'categorical_features': categorical_features, 'numeric_features': numeric_features}, 'model/model.pkl')
print("💾 Model saved as 'model/model.pkl'")