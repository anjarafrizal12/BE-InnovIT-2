import os
from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO

app = Flask(__name__)

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
        # Membaca file Excel langsung dari bytes (tanpa menyimpannya ke disk)
        try:
            df = pd.read_excel(BytesIO(file.read()))
            # Mengonversi data Excel menjadi dictionary
            global data_array
            data_array = df.to_dict(orient='records')
            return jsonify({"message": "File uploaded successfully", "data": data_array}), 200
        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 400
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
