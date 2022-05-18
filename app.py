from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from accountant import Manager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

db = SQLAlchemy(app)


# stworzenie tabeli na historię operacji
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


# zapis do bazy danych dotychczasowej historii operacji
def zapis_do_bazy_danych():     # TODO: póki nie stworzy się danej tabeli (flask db revision initial, flask db upgrade) i gdy to się uruchomi poniżej to nie stworzy się tabela (tworzy się plik bazy danych, ale bez tabeli)
    loaded_history = db.session.query(History).filter(History.id == 1).first()
    if not loaded_history:
        for polecenie in manager.historia_operacji:
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
            db.session.commit()


# zapisanie nowych danych z formularza internetowego
@app.route('/', methods=['GET', 'POST'])
def dane_z_formularza_internetowego():
    if request.method == "POST":
        if request.form["operation_type"] == "sprzedaz":
            name = request.form["name2"]
            price = request.form["price2"]
            quantity = request.form["quantity2"]
            polecenie = ("sprzedaz", name, price, quantity)
            manager.sprzedaz_func(polecenie)
        elif request.form["operation_type"] == "zakup":
            name = request.form["name1"]
            price = request.form["price1"]
            quantity = request.form["quantity1"]
            polecenie = ("zakup", name, price, quantity)
            manager.zakup_func(polecenie)
        elif request.form["operation_type"] == "saldo":
            name = request.form["name3"]
            price = request.form["price3"]
            polecenie = ("saldo", price, name)
            manager.saldo_func(polecenie)
        manager.historia_operacji.append(polecenie)
        if manager.error == 0:
            if polecenie[0] == "saldo":
                element_historii = History(operation_type="saldo", price=polecenie[1], product_name=polecenie[2])
            elif polecenie[0] == "zakup":
                element_historii = History(operation_type="zakup", product_name=polecenie[1], price=polecenie[2],
                                           quantity=polecenie[3])
            elif polecenie[0] == "sprzedaz":
                element_historii = History(operation_type="sprzedaz", product_name=polecenie[1], price=polecenie[2],
                                           quantity=polecenie[3])
            db.session.add(element_historii)
            db.session.commit()
        else:
            del manager.historia_operacji[-1]
            return redirect('/error/')
        return redirect('/')
    return render_template("main.html", magazyn=manager.magazyn, saldo=manager.saldo)


@app.route('/error/')
def error():
    return render_template("error.html"), {"Refresh": "4; url=/"}


@app.route('/historia/')
def historia():
    return render_template("historia.html", historia_operacji=manager.historia_operacji)


@app.route('/historia/<line_from>/<line_to>/')
def historia_przedzial(line_from, line_to):
    historia_czesc = manager.historia_operacji[int(line_from):int(line_to) + 1]
    return render_template("historia_przedzial.html",
                           historia_czesc=historia_czesc, line_from=line_from, line_to=line_to)


alembic = Alembic()
alembic.init_app(app)

manager = Manager("in.txt")

zapis_do_bazy_danych()


# do czyszczenia historii bazy danych
# db.session.query(History).filter(History.id > 0).delete()
# db.session.commit()
