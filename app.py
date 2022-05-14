from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

db = SQLAlchemy(app)


# creation a table of history of operations
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(120), nullable=False)
    amount_money = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


alembic = Alembic()
alembic.init_app(app)


# initial data on history of operations         # TODO: czy te początkowe dane mogą być wprowadzone po prostu z ręki?
his_saldo_1 = History(operation_type="saldo", amount_money=1000000, product_name="wplata poczatkowa")
his_saldo_2 = History(operation_type="saldo", amount_money=-140000, product_name="zus")
his_zakup_1 = History(operation_type="zakup", product_name="raspberry", amount_money=15000, quantity=5)
his_sprzedaz_1 = History(operation_type="sprzedaz", product_name="raspberry", amount_money=25000, quantity=5)
his_zakup_2 = History(operation_type="zakup", product_name="jetson", amount_money=40000, quantity=5)
his_sprzedaz_2 = History(operation_type="sprzedaz", product_name="jetson", amount_money=50000, quantity=1)
# db.session.add(his_saldo_1)
# db.session.query(History).filter(History.id == 2).delete()
# db.session.add(his_saldo_2)
# db.session.add(his_zakup_1)
# db.session.add(his_sprzedaz_1)
# db.session.add(his_zakup_2)
# db.session.add(his_sprzedaz_2)


db.session.commit()
