# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

# Create a dummy dataset (for example: health risk prediction)
# You can replace this with real data later
np.random.seed(42)
data = pd.DataFrame({
    'age': np.random.randint(20, 70, 100),
    'bmi': np.random.uniform(18, 35, 100),
    'bp': np.random.randint(80, 160, 100),
    'glucose': np.random.randint(70, 200, 100),
    'risk': np.random.randint(0, 2, 100)  # 0 = low risk, 1 = high risk
})

# Split the data
