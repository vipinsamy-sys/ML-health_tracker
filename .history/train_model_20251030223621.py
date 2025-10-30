import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

print("Starting model training...")

# Dummy dataset with all inputs
np.random.seed(42)
data = pd.DataFrame({
    'age': np.random.randint(20, 70, 200),
    'gender': np.random.choice(['Male', 'Female', 'Other'], 200),
    'bmi': np.random.uniform(18, 35, 200),
    'bp': np.random.randint(80, 160, 200),
    'glucose': np.random.randint(70, 200, 200),
    'activity': np.random.choice(['Low', 'Moderate', 'High'], 200),
    'habits': np.random.choice(['Yes', 'No'], 200),
    'risk': np.random.randint(0, 2, 200)
})

print("Dataset created successfully")

# Encode categorical columns
le_gender = LabelEncoder()
le_activity = LabelEncoder()
le_habits = LabelEncoder()

data['gender'] = le_gender.fit_transform(data['gender'])
data['activity'] = le_activity.fit_transform(data['activity'])
data['habits'] = le_habits.fit_transform(data['habits'])

X = data[['age', 'gender', 'bmi', 'bp', 'glucose', 'activity', 'habits']]
y = data['risk']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print(f"✅ Model trained successfully with accuracy: {acc*100:.2f}%")

# Save model and encoders
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/model.pkl')
joblib.dump(le_gender, 'model/le_gender.pkl')
joblib.dump(le_activity, 'model/le_activity.pkl')
joblib.dump(le_habits, 'model/le_habits.pkl')

print("💾 Model and encoders saved successfully in 'model/' folder")
