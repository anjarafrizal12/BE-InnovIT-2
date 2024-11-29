import os
from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
from flask_cors import CORS
import googlemaps

app = Flask(__name__)

CORS(app)

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
      resultgoogle = cek_jarak(row['LatLong'])
      print(resultgoogle["rows"][0]["elements"][0]["distance"]["text"])
      # df_base['Jarak'] = resultgoogle["rows"][0]["elements"][0]["distance"]["text"]
      print(resultgoogle['rows'][0]['elements'][0]['duration']['value'])
      duration_seconds = resultgoogle['rows'][0]['elements'][0]['duration']['value']
      distance = resultgoogle["rows"][0]["elements"][0]["distance"]["text"]
      duration_minutes = duration_seconds / 60

      df_base.loc[index, 'EstimasiReal'] = duration_minutes
      df_base.loc[index, 'Jarak'] = distance
      df_base.loc[index, 'Estimasi'] = resultgoogle['rows'][0]['elements'][0]["duration"]["text"]
      

      if round(duration_minutes) <= 120:
        if index > 0:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=6))
          time_backwards = waktu - timedelta(minutes=duration_minutes-30)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P1"
        else:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=6))
          time_backwards = waktu - timedelta(minutes=duration_minutes)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P1"
        
      elif round(duration_minutes) > 120 and round(duration_minutes) <= 240:
        if index > 0:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=9))
          time_backwards = waktu - timedelta(minutes=duration_minutes-30)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P2"
        else:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=9))
          time_backwards = waktu - timedelta(minutes=duration_minutes)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P2"
      elif round(duration_minutes) > 240 and round(duration_minutes) <= 360:
        if index > 0:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=12))
          time_backwards = waktu - timedelta(minutes=duration_minutes-30)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P3"
        else:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=12))
          time_backwards = waktu - timedelta(minutes=duration_minutes)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P3"
      else:
        if index > 0:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=15))
          time_backwards = waktu - timedelta(minutes=duration_minutes-30)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P4"
        else:
          waktu = datetime.combine(datetime.today(), datetime.min.time().replace(hour=15))
          time_backwards = waktu - timedelta(minutes=duration_minutes)
          formatted_time = time_backwards.strftime("%H:%M")
          df_base.loc[index, 'Rekomendasi'] = "Anda diharuskan berangkat menuju plant sunter : "+str(formatted_time)
          df_base.loc[index, 'Period'] = "S1P4"

      
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
    df_base_sorted = df_base.sort_values(by=['Period', 'EstimasiReal'], ascending=[True, True])
    data_array = df_base_sorted.to_dict(orient='records')
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
            df_base['Jarak'] = "-"
            df_base['Estimasi'] = "-"
            df_base['Period'] = "-"
            df_base['Rekomendasi'] = "-"
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
