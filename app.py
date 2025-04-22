from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    gavetas = db.Column(db.Integer, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/api/ingreso", methods=["POST"])
def ingresar_producto():
    data = request.json
    try:
        nuevo = Producto(
            tipo=data["tipo"],
            fecha=datetime.strptime(data["fecha"], "%Y-%m-%d").date(),
            peso=float(data["peso"]),
            gavetas=int(data["gavetas"])
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"mensaje": "Producto registrado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/inventario", methods=["GET"])
def ver_inventario():
    productos = Producto.query.all()
    resultado = [
        {
            "id": p.id,
            "tipo": p.tipo,
            "fecha": p.fecha.strftime("%Y-%m-%d"),
            "peso": p.peso,
            "gavetas": p.gavetas,
            "fecha_ingreso": p.fecha_ingreso.strftime("%Y-%m-%d %H:%M")
        } for p in productos
    ]
    return jsonify(resultado)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)