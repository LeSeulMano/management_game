from flask import render_template, request, session, redirect, jsonify
from middleware.usersModel import logged_in, is_credential_correct, setoken
from middleware.encryption import hash_shab512, token
from middleware.villageModel import village_data, village_update
from middleware.ressourcesModel import update_ressources, mange
from middleware.centreModel import addWork, removeWork, addCentre
from middleware.personModel import add_pers
from middleware.houssesModel import addHouses
from middleware.entrepotModel import entrepot_levelup
from lib.init_routes import app


@app.route("/")
def index():
    if not logged_in():
        return redirect("/login")
    return render_template("index.html", foo=42)

@app.route("/village/<user_id>")
def village(user_id):
    return village_data(user_id)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/leave", methods=["POST"])
def leave():
    time = request.json['time']
    village_update(time)
    return "Leave success !"

@app.route("/update_ressources/<user_id>")
def ressources(user_id):
    if user_id == "0":
        return update_ressources()
    else:
        if user_id == "1":
            return mange()
        return 'ok'
    
@app.route("/addwork/<ferme>")
def addwork(ferme):
    return addWork(ferme)

@app.route("/removework/<ferme>")
def removework(ferme):
    return removeWork(ferme)

@app.route("/addpers")
def addpers():
    return add_pers()

@app.route("/addhouses/<bool>")
def addhouse(bool):
    return addHouses(bool)

@app.route("/levelup/<bool>")
def levelup(bool):
    return entrepot_levelup(bool)

@app.route("/addusine/<usine>")
def addusine(usine):
    return addCentre(usine, True)

@app.route("/finishusine/<usine>")
def finishusine(usine):
    return addCentre(usine, False)


@app.route("/login/auth", methods=["POST"])
def login_auth():
    login = request.json['login']
    psswd = request.json['password']
    psswd = hash_shab512(psswd)
    if (is_credential_correct(login, psswd)):
        token_user = token(login)
        setoken(login, token_user)
        session["TOKEN"] = token_user
        token_info = {
            'access_token': '...',
            'refresh_token': '...',
            'token_type': '...',
            'expires_in': '...' 
        }
        return redirect(
            '/',
            302,
            jsonify(token_info)
        )
    else:
        print("error")
        return "Connexion refused"
    
@app.route("/logout")
def logout():
    session.clear()
    return "Logout !"
