from flask import Flask
from flask import request, jsonify, json
from pymongo import MongoClient


app = Flask(__name__)

#untuk menghubungkan ke MongoDB
client = MongoClient("mongodb+srv://Pemburu_Mimpi:putriaulia310508@cluster0.bnt35.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["MyDatabase"]
collection = db["MyCollection"]

# send to Ubidots/Mengirimkan ke Ubidots
UBIDOTS_TOKEN = "BBUS-bcMg6vofNXBrwsbWtZJXhPjpPb5MGj"
DEVICE_LABEL = "esp32-mimpi"
UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/esp32-mimpi"
UBIDOTS_HEADERS = {
    'X-Auth-Token': UBIDOTS_TOKEN,
    'Content-Type': 'application/json' 
}

#Menerima data : suhu,kelembaban, dan intensitas cahaya dari ESP32
@app.route("/api/dht", methods=["POST"])
def receive_data():
    data = request.json
    temperature = data["temperature"]
    humidity = data["humidity"]
    light_value = data["light_value"]
    collection.insert_one(data)
    ubidots_payload = {
        "temperature": temperature,
        "humidity": humidity,
        "light_value": light_value
        }

    ubidots_response = requests.post(UBIDOTS_URL, headers=UBIDOTS_HEADERS, json=ubidots_payload)
    print(ubidots_response.text)
    
    return jsonify({"message": "Data saved", "ubidots_response":ubidots_response.json()}), 201

#Mengambil data dari database MongoDB
@app.route("/api/dht", methods=["GET"])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)