from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('model/model.pkl')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = float(request.form['age'])
        bmi = float(request.form['bmi'])
        bp = float(request.form['bp'])
        glucose = float(request.form['glucose'])

        input_data = np.array([[age, bmi, bp, glucose]])
        prediction = model.predict(input_data)[0]

        result = "⚠️ High Risk" if prediction == 1 else "✅ Low Risk"
        return render_template('index.html', result=result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
