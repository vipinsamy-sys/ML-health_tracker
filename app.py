from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import os

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

app = Flask(__name__)

model_bundle = joblib.load('model/model.pkl')
pipeline = model_bundle['pipeline']
categorical_features = model_bundle['categorical_features']
numeric_features = model_bundle['numeric_features']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract fields from form, matching training feature names
        form = request.form

        def get_select(name):
            return (form.get(name) or '').strip()

        def get_float(name, default=None):
            val = (form.get(name) or '').strip().lower().replace('l', '')
            if val == '':
                return default
            return float(val)

        # Required height/weight
        height_cm = get_float('height_cm')
        weight_kg = get_float('weight_kg')
        if height_cm is None or weight_kg is None:
            return jsonify({'error': 'height_cm and weight_kg are required'}), 400
        bmi = None
        try:
            h_m = height_cm / 100.0
            if h_m > 0:
                bmi = round(weight_kg / (h_m * h_m), 1)
        except Exception:
            return jsonify({'error': 'Invalid height/weight values'}), 400

        row = {
            'gender': get_select('gender'),
            'body_type': get_select('body_type'),
            'diet_type': get_select('diet_type'),
            'physical_activity': get_select('physical_activity'),
            'family_history': get_select('family_history'),
            'stress_level': get_select('stress_level'),
            'smoking': get_select('smoking'),
            'alcohol': get_select('alcohol'),
            'junk_food_freq': get_select('junk_food_freq'),
            'age': get_float('age'),
            'sleep_hours': get_float('sleep_hours'),
            'water_intake_liters': get_float('water_intake_liters'),
            'bmi': bmi,
            'height_cm': height_cm,
            'weight_kg': weight_kg,
            'glucose': get_float('glucose'),
            'systolic_bp': get_float('systolic_bp'),
            'diastolic_bp': get_float('diastolic_bp'),
            'sugar': get_float('sugar'),
        }

        # Create DataFrame with correct column order
        import pandas as pd
        X = pd.DataFrame([row], columns=categorical_features + numeric_features)

        prediction = pipeline.predict(X)[0]
        result = "⚠️ High Risk" if int(prediction) == 1 else "✅ Low Risk"
        return render_template('index.html', result=result)

    except Exception as e:
        return jsonify({'error': str(e)})

# Simple chat endpoint that proxies to OpenAI's Chat Completions API
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if OpenAI is None:
            return jsonify({ 'error': 'OpenAI SDK not installed. Run: pip install openai>=1.40.0' }), 500

        data = request.get_json(silent=True) or {}
        user_message = (data.get('message') or '').strip()
        if not user_message:
            return jsonify({ 'error': 'message is required' }), 400

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return jsonify({ 'error': 'OPENAI_API_KEY environment variable not set' }), 500

        client = OpenAI(api_key=api_key)

        # System prompt tailored for health guidance disclaimers
        system_prompt = (
            "You are HealthBot, a helpful assistant for general wellness and education. "
            "Provide clear, empathetic, evidence-informed guidance. Do not offer diagnoses. "
            "Add a brief disclaimer to consult a medical professional for personal medical advice."
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,
            max_tokens=350,
        )

        reply = completion.choices[0].message.content if completion and completion.choices else "I'm sorry, I couldn't generate a response."

        # Minimal CORS support for local dev (so public/login.html on another port can call this)
        response = jsonify({ 'reply': reply })
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Vary'] = 'Origin'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response
    except Exception as e:
        response = jsonify({ 'error': str(e) })
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Vary'] = 'Origin'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response, 500

if __name__ == "__main__":
    app.run(debug=True)