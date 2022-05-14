from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from accountant import dotychczasowa_historia_operacji, historia_operacji

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

db = SQLAlchemy(app)


# creation a table of history of operations
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


def zapis_do_bazy_danych():
    dotychczasowa_historia_operacji()
    for polecenie in historia_operacji:
        if polecenie[0] == "saldo":
            element_historii = History(operation_type="saldo", price=polecenie[1], product_name=polecenie[2])
        elif polecenie[0] == "zakup":
            element_historii = History(operation_type="zakup", product_name=polecenie[1], price=polecenie[2],
                                       quantity=polecenie[3])
        elif polecenie[0] == "sprzedaz":
            element_historii = History(operation_type="sprzedaz", product_name=polecenie[1], price=polecenie[2],
                                       quantity=polecenie[3])
        else:
            break
        db.session.add(element_historii)


alembic = Alembic()
alembic.init_app(app)


zapis_do_bazy_danych()

db.session.commit()
