from flask import session
from lib.init_bdd import con


def logged_in() -> bool:
    token: str = session.get("TOKEN", None)
    if token:
        token_valid: bool = check_token_validity(token)
        if token_valid:
            return True
    return False

def check_token_validity(token):
    sql = "SELECT id, login FROM users WHERE token = %(token)s;"
    fdata = {
        "token": token
    }
    cr = con.cursor()
    res = cr.execute(sql, fdata)
    res = cr.fetchall()
    con.commit()
    cr.close()
    if not res: return False
    else: return True

def is_credential_correct(login, hashed_password) :
    sql = "SELECT id, login FROM users WHERE login = %(login)s AND password  = %(password)s;"
    fdata = {
        "login": login,
        "password": hashed_password
    }
    cr = con.cursor()
    res = cr.execute(sql, fdata)
    res = cr.fetchall()
    con.commit()
    cr.close()
    if not res: return False
    else: return True


def setoken(login, token):

    sql = "UPDATE users SET token = %(token)s WHERE login = %(login)s;"
    fdata = {
        "token": token,
        "login": login
    }
    cr = con.cursor()
    res = cr.execute(sql, fdata)
    con.commit()
    cr.close()
    return "Success !"

def removetoken(login):
    sql = "UPDATE users SET token = 0 WHERE login = %(login)s"