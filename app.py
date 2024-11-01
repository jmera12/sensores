from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

# Modelos de la base de datos
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all()

# Ruta para recibir datos de temperatura y humedad
@app.route('/api/sensores', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    temperature = data['temperature']
    humidity = data['humidity']
    
    nuevo_dato = SensorData(temperature=temperature, humidity=humidity)
    db.session.add(nuevo_dato)
    db.session.commit()

    return jsonify({"message": "Datos guardados correctamente"}), 201

# Ruta para recibir y guardar imágenes
@app.route('/api/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        new_image = ImageData(image_path=filename)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": "Imagen guardada exitosamente"}), 201
    return jsonify({"error": "No se recibió ninguna imagen"}), 400

# Ruta para obtener datos históricos
@app.route('/api/sensores', methods=['GET'])
def obtener_datos():
    registros = SensorData.query.order_by(SensorData.timestamp.desc()).all()
    data = [{"temperature": r.temperature, "humidity": r.humidity, "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for r in registros]
    return jsonify(data)

# Ruta para obtener imágenes
@app.route('/api/images/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para listar imágenes
@app.route('/api/images', methods=['GET'])
def list_images():
    images = ImageData.query.order_by(ImageData.timestamp.desc()).all()
    data = [{"image_path": r.image_path, "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for r in images]
    return jsonify(data)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
