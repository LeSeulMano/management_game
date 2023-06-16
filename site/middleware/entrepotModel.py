from lib.init_bdd import con
from flask import jsonify
from middleware.constructionModel import entrepot

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


def entrepot_levelup(start):
    if start == "True": 
        sql = "SELECT quantite, name_res FROM stock, ressources, entrepot, village WHERE (ressources.name_res = 'Bois' OR ressources.name_res = 'Fer' OR ressources.name_res = 'Pierre') AND ressources.id_ressources = stock.id_ressources AND stock.id_entrepot = entrepot.id_entrepot AND entrepot.id_village = village.id_village AND village.id_user = 1 ORDER BY name_res;"
        res = execute(sql, { })
        sql = "SELECT level_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1;"
        level = execute(sql, { })
        sql = "SELECT id_entrepot FROM entrepot, village WHERE entrepot.enconstruction = false AND entrepot.id_village = village.id_village AND village.id_user = 1;"
        id_entrepot = execute(sql, { })
        if len(id_entrepot) == 0:
            response = jsonify({'message': 'L\'entrepot est déjà en amélioration'})
            response.status_code = 400
            return response
        if (res[0][0] >= 50 + (level[0][0] - 1) * 10) and (res[1][0] >= 20 + (level[0][0] - 1) * 10) and (res[2][0] >= 50 + (level[0][0] - 1) * 10):
            start_build = entrepot(id_entrepot[0][0], True, level)
            if start_build[0]:
                sql = "UPDATE stock SET quantite = quantite - " + str(50 + (level[0][0] - 1) * 10) + " WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(id_entrepot[0][0]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Bois' OR ressources.name_res = 'Pierre'));"
                execute(sql, { })
                sql = "UPDATE stock SET quantite = quantite - " + str(20 + (level[0][0] - 1) * 10) + " WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(id_entrepot[0][0]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Fer'));"
                execute(sql, { })
                sql = "UPDATE entrepot SET enconstruction = true WHERE id_entrepot = " + str(id_entrepot[0][0])
                execute(sql, { })
            response = jsonify({'message': start_build[1]})
            response.status_code = start_build[2] 
            return response
        else:
            response = jsonify({'message': 'Pas les ressources necessaires !'})
            response.status_code = 400
            return response
    else:
        sql = "SELECT id_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1"
        id = execute(sql, { })
        sql = "UPDATE entrepot SET enconstruction = false, level_entrepot = level_entrepot + 1, capacite = capacite + 100 WHERE id_entrepot = " + str(id[0][0])
        execute(sql, { })
        start_build = entrepot(id[0][0], False, None)
        return 'Done'