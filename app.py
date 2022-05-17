from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from accountant import Manager

app = Flask(__name__)
manager = Manager("in.txt")

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

db = SQLAlchemy(app)

# saldo = 0
# magazyn = {"kot": 230, "wieloryb": 5}


# stworzenie tabeli na historię operacji
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)


# # zapis do bazy danych dotychczasowej historii operacji
# def zapis_do_bazy_danych():
#     loaded_history = db.session.query(History).filter(History.id == 1).first()
#     if not loaded_history:
#         # print("baza danych jest pusta")
#         dotychczasowa_historia_operacji()
#         for polecenie in historia_operacji:
#             if polecenie[0] == "saldo":
#                 element_historii = History(operation_type="saldo", price=polecenie[1], product_name=polecenie[2])
#             elif polecenie[0] == "zakup":
#                 element_historii = History(operation_type="zakup", product_name=polecenie[1], price=polecenie[2],
#                                            quantity=polecenie[3])
#             elif polecenie[0] == "sprzedaz":
#                 element_historii = History(operation_type="sprzedaz", product_name=polecenie[1], price=polecenie[2],
#                                            quantity=polecenie[3])
#             else:
#                 break
#             db.session.add(element_historii)
#             db.session.commit()
#         # print("wypełniam bazę danych...")
#         # historia_na_dzialania()
#         print(1, magazyn)
#         print(1, saldo)
#         print(1, historia_operacji)
#         return historia_operacji  # magazyn, saldo,
#     # print(2, magazyn)
#     # print(2, historia_operacji)
#     # print("baza danych jest już wypełniona historycznymi danymi!")


# zapisanie nowych danych z formularza internetowego
@app.route('/', methods=['GET', 'POST'])
def dane_z_formularza_internetowego():
    if request.method == "POST":
        if request.form["operacja"] == "sprzedaz":
            name = request.form["name2"]
            price = request.form["price2"]
            amount = request.form["amount2"]
            polecenie = ("sprzedaz", name, price, amount)
            manager.sprzedaz_func(polecenie)
        elif request.form["operacja"] == "zakup":
            name = request.form["name1"]
            price = request.form["price1"]
            amount = request.form["amount1"]
            polecenie = ("zakup", name, price, amount)
            manager.zakup_func(polecenie)
        elif request.form["operacja"] == "saldo":
            name = request.form["name3"]
            price = request.form["price3"]
            polecenie = ("saldo", price, name)
            manager.saldo_func(polecenie)
        manager.historia_operacji.append(polecenie)
        if manager.error == 0:
            manager.zapis_do_pliku()
        else:
            del manager.historia_operacji[-1]
            return redirect('/error/')
        return redirect('/')
    return render_template("main.html", magazyn=manager.magazyn, saldo=manager.saldo)

        # element_historii = History(operation_type="sprzedaz", product_name=product_name, price=product_price,
        #                            quantity=product_quantity)
        # db.session.add(element_historii)
        # if product_name in magazyn:
        #     if magazyn[product_name] >= int(product_quantity):
        #         # print("mamy tyle sztuk na sprzedaz")
        #         db.session.commit()
        #         # saldo += int(product_quantity) * int(product_price)
        #     else:
        #         print("za mało sztuk w magazynie")
        #
        # a = sum(db.session.query(History).filter(History.product_name == "sprzedaz").all())
        # print("tuuu:", a)
        # ilosc = 0
        # # lista =
        # for element in db.session.query(History).filter(History.operation_type == "zakup").all():
        #     ilosc += int(db.session.query(History).filter(History.quantity).element)
        #     print(ilosc)
        # if int(product_quantity) <= ilosc:   # TODO: tak jeśli mamy dany produkt do sprzedania
        #     print("mamy to")
        #     db.session.commit()
        # else:
        #     print("Błąd")
        # # print(magazyn)



alembic = Alembic()
alembic.init_app(app)


# zapis_do_bazy_danych()
#
# # historia_na_dzialania()
#
# hist = zapis_do_bazy_danych()
#
# print(3, magazyn)
# print(3, saldo)
# print(3, historia_operacji)
# print(4, hist)


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


# db.session.query(History).filter(History.id > 0).delete()
# db.session.commit()
