from lib.init_bdd import con
from middleware.constructionModel import build_house
from flask import Flask, jsonify

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

def addHouses(start):
    if start == "True":
        sql = "SELECT quantite, entrepot.id_entrepot FROM village, stock, ressources, entrepot WHERE (ressources.name_res = 'Bois' OR ressources.name_res = 'Pierre') AND ressources.id_ressources = stock.id_ressources AND stock.id_entrepot = entrepot.id_entrepot AND entrepot.id_village = village.id_village AND village.id_user = 1 ORDER BY name_res;"
        res = execute(sql, { })
        sql = "SELECT id_maison FROM maison, village WHERE village.id_user = 1 AND village.id_village = maison.id_village AND maison.enconstruction = true;"
        tmp = execute(sql, { })
        if len(tmp) != 0:
            response = jsonify({'message': 'Une maison est déjà en train d\'être construite !'})
            response.status_code = 400
            return response
        sql = "SELECT nb_maison FROM village WHERE village.id_user = 1;"
        nb_house = execute(sql, { })
        if (res[0][0] >= 20 + (nb_house[0][0] - 6) * 10) and (res[1][0] >= 20 + (nb_house[0][0] - 6) * 10):

            start_build = build_house(None, True)
            if start_build[0]:
                sql = "UPDATE stock SET quantite = quantite - " + str(20 + (nb_house[0][0] - 6) * 10) + " WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(res[0][1]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Bois' OR ressources.name_res = 'Pierre'));"
                execute(sql, { })
            response = jsonify({'message': start_build[1]})
            response.status_code = start_build[2] 
            return response
        else:
            response = jsonify({'message': 'Pas les ressources necessaires !'})
            response.status_code = 400
            return response
        
    else:
        sql = "UPDATE village SET nb_maison = nb_maison + 1 WHERE village.id_user = 1;"
        execute(sql, { })
        sql = "SELECT id_maison FROM maison, village WHERE village.id_user = 1 AND village.id_village = maison.id_village AND maison.enconstruction = true;"
        house = execute(sql, { })
        sql = "UPDATE maison SET enconstruction = false WHERE id_maison = " + str(house[0][0])
        execute(sql, { })
        start_build = build_house(house[0][0], False)
        return 'Done'