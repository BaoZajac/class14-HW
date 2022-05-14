from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(app)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(120), nullable=False)
    figure = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


alembic = Alembic()
alembic.init_app(app)

