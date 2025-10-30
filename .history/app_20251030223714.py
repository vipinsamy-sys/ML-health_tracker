from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model and encoders
model = joblib.load('model/model.pkl')
le_gender = joblib.load('model/le_gender.pkl')
le_activity = joblib.load('model/le_activity.pkl')
le_habits = joblib.load('model/le_habits.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = float(request.form['age'])
        gender = request.form['gender']
        bmi = float(request.form['bmi'])
        bp = float(request.form['bp'])
        glucose = float(request.form['glucose'])
        activity = request.form['activity']
        habits = request.form['habits']

        # Encode categorical inputs
        gender_encoded = le_gender.transform([gender])[0]
        activity_encoded = le_activity.transform([activity])[0]
        habits_encoded = le_habits.transform([habits])[0]

        # Prepare input array
        input_data = np.array([[age, gender_encoded, bmi, bp, glucose, activity_encoded, habits_encoded]])

        prediction = model.predict(input_data)[0]
        result = "⚠️ High Risk" if prediction == 1 else "✅ Low Risk"

        return render_template('index.html', result=result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
