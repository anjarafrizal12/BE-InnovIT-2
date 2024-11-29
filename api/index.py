import os
from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO
import googlemaps

app = Flask(__name__)

# Array untuk menyimpan data
df_base = None

API_KEY = 'AIzaSyACzawZOpNwNB58pQoa28lFhp89Yor5aVI'
gmaps = googlemaps.Client(key=API_KEY)
origin = "-6.903710712010781, 107.56704420278929"
destination = "-6.161668392129037, 106.88097402522885"

def cek_jarak(coordinate):
  result = gmaps.distance_matrix(origins=coordinate,
                                destinations=destination,
                                mode="driving",
                                language="id",
                                units="metric")
  return result

@app.route('/process', methods=['POST'])
def process_data():
  try:
    
    # df_base = pd.read_excel(BytesIO(file.read()))

    for index, row in df_base.iterrows():
      # print(row['Lat Long'])
      resultgoogle = cek_jarak(row['Lat Long'])
      print(result["rows"][0]["elements"][0]["distance"]["text"])
      print(resultgoogle['rows'][0]['elements'][0]['duration']['value'])
      duration_seconds = resultgoogle['rows'][0]['elements'][0]['duration']['value']
      distance = resultgoogle["rows"][0]["elements"][0]["distance"]["text"]
      duration_minutes = duration_seconds / 60

      if round(duration_minutes) <= 120:
        df_base['Period'] = "S1P1"
      elif round(duration_minutes) > 120 and round(duration_minutes) <= 240:
        df_base['Period'] = "S1P2"
      elif round(duration_minutes) > 240 and round(duration_minutes) <= 360:
        df_base['Period'] = "S1P3"
      else:
        df_base['Period'] = "S1P4"

      
      # array_jarak.append(distance)
      # array_est.append(df_base.apply(resultgoogle['rows'][0]['elements'][0]['duration']['value']))
      # array_recomm.append("Anda sebaiknya berangkat puluk 05:30")
      # df_base['Estimasi'] = df_base.apply(resultgoogle['rows'][0]['elements'][0]['duration']['value'])
      # df_base['Rekomendasi'] = "Anda sebaiknya berangkat puluk 05:30"
            # Mengonversi data Excel menjadi dictionary
    # df_base['Jarak'] = array_jarak
    # df_base['Estimasi'] = array_est
    # df_base['Recomm'] = array_recomm
    # df_base['Period'] = array_period
    global data_array
    data_array = df_base.to_dict(orient='records')
    return jsonify({"message": "File uploaded successfully", "data": data_array}), 200
  except Exception as e:
    return jsonify({"error": f"Error processing file: {str(e)}"}), 400
  

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
            global df_base
            df_base = pd.read_excel(BytesIO(file.read()))
            # df['Jarak'] = "145 km"
            # df['Estimasi'] = "1 Jam 45 Menit"
            # df['Period'] = "S1P1"
            # df['Rekomendasi'] = "Anda sebaiknya berangkat puluk 05:30"
            # Mengonversi data Excel menjadi dictionary
            global data_array
            data_array = df_base.to_dict(orient='records')
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
