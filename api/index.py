import os
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Tempat penyimpanan file upload sementara
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Array untuk menyimpan data
data_array = []

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Baca file Excel dengan pandas
        df = pd.read_excel(file_path)
        
        # Misalkan data yang diambil adalah semua baris dan kolom Excel
        global data_array
        data_array = df.to_dict(orient='records')
        
        return jsonify({"message": "File uploaded successfully", "data": data_array}), 200
    else:
        return jsonify({"error": "Invalid file format. Please upload an Excel file."}), 400

@app.route('/get-data', methods=['POST'])
def get_data():
    if not data_array:
        return jsonify({"error": "No data available. Please upload a file first."}), 400
    
    return jsonify({"data": data_array}), 200

# Untuk Vercel, kita harus menggunakan WSGI handler.
if __name__ == '__main__':
    app.run(debug=True)
