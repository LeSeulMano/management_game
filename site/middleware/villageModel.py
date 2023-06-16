from lib.init_bdd import con

def village_data(user_id):
    data = {
        "stock": getStock(),
        "factory": getFactory(),
        "house": getHouses(),
        "nbhabitant": getHab(),
        "level_entre": getLevel(),
        "timer": getTime(),
        "working": getWork()
    }
    return data

def execute(sql, fdata):
    cr = con.cursor()
    res = cr.execute(sql, fdata)
    try: 
        res = cr.fetchall()
    except: 
        res = None
    con.commit()
    cr.close()
    return res

def getStock():
    sql = "SELECT name_res, quantite FROM entrepot, ressources, stock, village WHERE village.id_user = 1 AND entrepot.id_village = village.id_village AND stock.id_entrepot = entrepot.id_entrepot AND stock.id_ressources = ressources.id_ressources"
    return execute(sql, {})

def getFactory():
    sql = "SELECT nb_employee, type_usine, nbmax FROM centre, village WHERE village.id_user = 1 AND village.id_village = centre.id_village AND centre.enconstruction = false;"
    return execute(sql, {})

def getHouses():
    sql = "SELECT id_maison, nb_habitant FROM village, maison WHERE village.id_user = 1 AND maison.enconstruction = false ORDER BY id_maison"
    return execute(sql, {})

def getHab():
    sql = "SELECT COUNT(*) FROM habitant, maison, village WHERE village.id_user = 1 AND village.id_village = maison.id_village AND maison.id_maison = habitant.id_maison"
    return execute(sql, {})

def getLevel():
    sql = "SELECT level_entrepot, capacite FROM entrepot, village WHERE village.id_user = 1 AND village.id_village = entrepot.id_village"
    return execute(sql, {})

def getTime():
    sql = "SELECT timer FROM village WHERE village.id_user = 1"
    return execute(sql, {})


def village_update(time):
    sql = "UPDATE village SET timer = '" + time + "' WHERE village.id_user = 1;"
    return execute(sql, {})

def getWork():
    sql = "SELECT COUNT(*) FROM habitant, maison, village WHERE habitant.id_centre IS NULL AND village.id_user = 1 AND village.id_village = maison.id_village AND maison.id_maison = habitant.id_maison"
    return execute(sql, {})