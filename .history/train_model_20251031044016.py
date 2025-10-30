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

# Create larger, more realistic dataset with correlated features
np.random.seed(42)
N = 5000

age = np.random.randint(18, 80, N)
gender = np.random.choice(['Male', 'Female', 'Other'], N, p=[0.48, 0.50, 0.02])

# Age affects body type probability slightly
body_type = np.where(
    age > 50,
    np.random.choice(['Slim', 'Average', 'Overweight'], N, p=[0.15, 0.45, 0.40]),
    np.random.choice(['Slim', 'Average', 'Overweight'], N, p=[0.30, 0.55, 0.15])
)

diet_type = np.random.choice(['Vegetarian', 'Mixed', 'Fast-food lover'], N, p=[0.3, 0.45, 0.25])

# Physical activity linked with body type
physical_activity = np.where(
    body_type == 'Overweight',
    np.random.choice(['Rarely', 'Sometimes', 'Regularly'], N, p=[0.45, 0.45, 0.10]),
    np.random.choice(['Rarely', 'Sometimes', 'Regularly'], N, p=[0.20, 0.55, 0.25])
)

# Smoking/alcohol influence sleep
smoking = np.random.choice(['Yes', 'No'], N, p=[0.18, 0.82])
alcohol = np.random.choice(['Yes', 'No'], N, p=[0.30, 0.70])

sleep_hours = np.clip(
    np.random.normal(7 - (smoking == 'Yes') * 0.8 - (alcohol == 'Yes') * 0.5, 1.1, N),
    3.5, 10.0
)

family_history = np.where(
    age > 50,
    np.random.choice(['None', 'Diabetes', 'Heart Issues'], N, p=[0.45, 0.35, 0.20]),
    np.random.choice(['None', 'Diabetes', 'Heart Issues'], N, p=[0.60, 0.25, 0.15])
)

stress_level = np.random.choice(['Low', 'Medium', 'High'], N, p=[0.35, 0.45, 0.20])

# Correlated with diet and stress
water_intake_liters = np.clip(
    np.random.normal(2.8 - (stress_level == 'High') * 0.6 - (diet_type == 'Fast-food lover') * 0.5, 0.8, N),
    0.8, 5.5
)

junk_food_freq = np.where(
    diet_type == 'Fast-food lover',
    np.random.choice(['Rarely', 'Weekly', 'Daily'], N, p=[0.15, 0.40, 0.45]),
    np.random.choice(['Rarely', 'Weekly', 'Daily'], N, p=[0.55, 0.35, 0.10])
)

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

# Generate synthetic risk score with realistic influence
risk_score = (
    (age > 55).astype(int) * 0.8 +
    (body_type == 'Overweight').astype(int) * 0.9 +
    (diet_type == 'Fast-food lover').astype(int) * 0.8 +
    (physical_activity == 'Rarely').astype(int) * 0.9 +
    (sleep_hours < 6).astype(int) * 0.6 +
    (smoking == 'Yes').astype(int) * 0.9 +
    (alcohol == 'Yes').astype(int) * 0.4 +
    (family_history != 'None').astype(int) * 0.8 +
    (stress_level == 'High').astype(int) * 0.7 +
    (water_intake_liters < 2).astype(int) * 0.5 +
    (junk_food_freq == 'Daily').astype(int) * 0.7
)

# Convert score to probability and then binary label
noise = np.random.normal(0, 0.3, N)
prob = 1 / (1 + np.exp(-(risk_score + noise - 1.6)))
risk = (np.random.rand(N) < prob).astype(int)

data['risk'] = risk

print(f"✅ Dataset generated with {len(data)} samples and realistic lifestyle correlations.")

# Optional: basic sanity stats
print("Feature snapshot:")
print(data.head(3))

# Optional OpenAI validation (runs only if SDK/key available)
try:
    from openai import OpenAI as _OpenAI
    _api_key = os.environ.get('OPENAI_API_KEY')
    if _api_key:
        client = _OpenAI(api_key=_api_key)
        # Summarize distributions briefly to keep prompt small
        desc = data.describe(include='all').to_string()[:4000]
        prompt = (
            "You are a data QA assistant. Given summary stats of a synthetic health-risk dataset, "
            "check if feature distributions and correlations look plausible (not exact science). "
            "Only flag obviously unrealistic patterns. Reply in one short paragraph.\n\n" + desc
        )
        try:
            _resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a terse data QA assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
                max_tokens=180,
            )
            _msg = _resp.choices[0].message.content if _resp and _resp.choices else "(no validation response)"
            print("🔎 OpenAI validation:", _msg)
        except Exception as _e:
            print("(OpenAI validation skipped:", str(_e), ")")
except Exception:
    pass

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