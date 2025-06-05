from flask import Flask, render_template, request, session
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

model = joblib.load('model/ids_model.pkl')

global_intrusion_alert = False

@app.route('/')
def index():
    if global_intrusion_alert:
        return render_template('result.html', intrusion=True)
    else:
        return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global global_intrusion_alert
    try:
        features = request.json.get('features')
        prediction = model.predict([features])[0]
        intrusion = bool(prediction)

        global_intrusion_alert = intrusion  # <-- Works across curl + browser
        return {"intrusion": intrusion}

    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/reset')
def reset_alert():
    global global_intrusion_alert
    global_intrusion_alert = False
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
