# train_model.py
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

# Example dummy dataset
X = np.array([[18, 20], [45, 25], [60, 35], [30, 22], [50, 31]])
y = np.array([0, 1, 1, 0, 1])  # 0 = Low risk, 1 = High risk

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'model.pkl')
print("✅ Model trained and saved as model.pkl")
