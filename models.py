from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    gavetas = db.Column(db.Integer, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())