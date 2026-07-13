from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_from_directory
app = Flask(__name__)

# =====================================
# Load Trained Model
# =====================================

model = joblib.load("models/heart_model.pkl")

# =====================================
# Generate PDF Report
# =====================================

def generate_pdf(patient_name, prediction, confidence, recommendation):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/{patient_name.replace(' ','_')}_Heart_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>Heart Disease Prediction Report</b>",
            styles['Title']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Patient Name :</b> {patient_name}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Date :</b> {datetime.now().strftime('%d-%m-%Y')}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Time :</b> {datetime.now().strftime('%I:%M %p')}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Prediction :</b> {prediction}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"<b>Confidence :</b> {confidence:.2f} %",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            "<b>Health Recommendation</b>",
            styles['Heading2']
        )
    )

    for tip in recommendation:
        elements.append(
        Paragraph(f"• {tip}", styles["BodyText"])
    )

    doc.build(elements)

    return filename

# =====================================
# Recommendation Generator
# =====================================

def generate_recommendation(data, prediction):

    tips = []

    if prediction == 1:

        tips.append("Consult a cardiologist as soon as possible.")

        if data["chol"] > 240:
            tips.append("Reduce cholesterol-rich foods.")

        if data["trestbps"] > 140:
            tips.append("Monitor your blood pressure regularly.")

        if data["fbs"] == 1:
            tips.append("Maintain healthy blood sugar levels.")

        if data["exang"] == 1:
            tips.append("Avoid strenuous physical activities until medical advice.")

        if data["age"] > 50:
            tips.append("Schedule regular heart health check-ups.")

        tips.append("Walk at least 30 minutes daily.")
        tips.append("Avoid smoking.")
        tips.append("Limit alcohol consumption.")
        tips.append("Maintain a balanced diet.")
        tips.append("Manage stress through yoga or meditation.")

    else:

        tips.append("Excellent! Your predicted risk is low.")

        tips.append("Continue regular physical exercise.")
        tips.append("Eat a balanced diet rich in fruits and vegetables.")
        tips.append("Maintain healthy body weight.")
        tips.append("Avoid smoking.")
        tips.append("Drink enough water.")
        tips.append("Sleep 7-8 hours daily.")
        tips.append("Go for regular health check-ups.")

    return tips
# =====================================
# Home Page
# =====================================

@app.route("/")
def home():
    return render_template("index.html")

# =====================================
# Prediction API
# =====================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        patient_name = data.get("patient_name", "Patient")

        features = np.array([[
            float(data["age"]),
            float(data["sex"]),
            float(data["cp"]),
            float(data["trestbps"]),
            float(data["chol"]),
            float(data["fbs"]),
            float(data["restecg"]),
            float(data["thalach"]),
            float(data["exang"]),
            float(data["oldpeak"]),
            float(data["slope"]),
            float(data["ca"]),
            float(data["thal"])
        ]])


        # Prediction
        prediction = int(model.predict(features)[0])

        # Confidence
        confidence = float(max(model.predict_proba(features)[0]) * 100)

        if prediction == 1:
            prediction_text = "🔴 High Risk of Heart Disease"
        else:
            prediction_text = "🟢 Low Risk of Heart Disease"

        # Recommendation
        recommendation_list = generate_recommendation(data, prediction)

        pdf_path = generate_pdf(
    patient_name,
    prediction_text,
    confidence,
    recommendation_list
)

        return jsonify({

        "success": True,

        "prediction": prediction,

        "prediction_text": prediction_text,

        "confidence": round(confidence,2),

        "recommendation": "<br>".join(recommendation_list),

        "download_url": f"/download/{os.path.basename(pdf_path)}"

    })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500


import os

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        "reports",
        filename,
        as_attachment=True
    )
# =====================================
# Run Flask
# =====================================


if __name__ == "__main__":

    app.run(debug=True)