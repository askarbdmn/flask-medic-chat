from flask import Flask, request, jsonify
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np

# Load Model dan Tokenizer
model_path = "intent_classification_model"  # Sesuaikan dengan path model di Render
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()

# Mapping Label Intent
intent_labels = ["sapaan", "keluhan_kesehatan", "info_penyakit", "rekomendasi_tindakan"]

# Fungsi Prediksi Intent
def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return intent_labels[predicted_class]

# Inisialisasi Flask
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    user_text = data.get("text", "")
    if not user_text:
        return jsonify({"error": "Teks tidak boleh kosong"}), 400
    intent = predict_intent(user_text)
    return jsonify({"intent": intent})

# Menjalankan API Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
