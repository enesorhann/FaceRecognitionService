from flask import Flask, request, jsonify
import cv2
import face_recognition
import numpy as np
import requests
import io
from google.cloud import storage
import os


app = Flask(__name__)

storage_client = storage.Client()
bucket_name = "donemprojesi-2c535.firebasestorage.app" 

def download_image_from_url(image_url):
    try:
        response = requests.get(image_url)
        image_data = response.content
        img = np.asarray(bytearray(image_data), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)  # URL'den gelen resmi çözümle
        return img
    except Exception as e:
        print(f"Image download error: {str(e)}")
        raise

@app.route('/recognize', methods=['POST'])
def recognize_face():
    strg_url = request.form.get('strg_url')  # image_id parametresi olarak Firebase Storage URL'sini alıyoruz
    if not strg_url:
        return jsonify({"success": False, "error": "strg_url eksik"}), 400

    try:
        # Firebase Storage URL'sinden resmi indir
        img_from_storage = download_image_from_url(strg_url)
    except Exception as e:
        return jsonify({"success": False, "error": f"Image download error: {str(e)}"}), 500

    file = request.files.get('image')  # Kameradan gelen resmi al
    if not file:
        return jsonify({"success": False, "error": "Resim eksik"}), 400

    img_from_camera = np.frombuffer(file.read(), np.uint8)  # Kameradan gelen resmi byte dizisine dönüştür
    img_from_camera = cv2.imdecode(img_from_camera, cv2.IMREAD_COLOR)  # Resmi çözümle

    response = {"success": True, "detected": False}
    try:
        # Storage'deki yüzleri encode et
        encodings_storage = face_recognition.face_encodings(img_from_storage)
        if len(encodings_storage) == 0:
            return jsonify({"success": False, "error": "Storage'de yüz bulunamadi"}), 500
        encode_storage = encodings_storage[0]

        # Kameradan gelen yüzü encode et
        encodings_camera = face_recognition.face_encodings(img_from_camera)
        if len(encodings_camera) == 0:
            return jsonify({"success": False, "error": "Kamerada yüz bulunamadi"}), 500
        encode_camera = encodings_camera[0]

        # Yüz karşılaştırmasını yap
        matches = face_recognition.compare_faces([encode_storage], encode_camera)
        if matches[0]:  # Yüz eşleşirse
            response["detected"] = True
        else:
            response["detected"] = False

    except Exception as e:
        response["success"] = False
        response["error"] = f"Yüz tanima hatasi: {str(e)}"

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloud Run PORT'u okur
    app.run(host='0.0.0.0', port=port)       # 0.0.0.0 adresinde çalışır
