from lib.init_bdd import con
from flask import jsonify
from middleware.constructionModel import centre

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

def addWork(ferme):
    sql = "SELECT id_centre, nb_employee, nbmax FROM centre, village WHERE centre.enconstruction = false AND village.id_user = 1 AND village.id_village = centre.id_village AND centre.type_usine = '" + ferme + "';"
    res = execute(sql, { })
    for i in range (len(res)):
        if res[i][1] != res[i][2]:
            try:
                sql = "SELECT id_habitant FROM habitant, village, maison WHERE habitant.id_factory_build IS NULL AND habitant.id_entrepot_build IS NULL AND habitant.id_centre IS NULL AND village.id_user = 1 AND village.id_village = maison.id_village AND maison.id_maison = habitant.id_maison;"
                tmp = execute(sql, { })
                if len(tmp) == 0: 
                    return 'Tous les habitants travaille déjà !'
                sql = "UPDATE habitant SET id_centre = " + str(res[i][0]) + " WHERE id_factory_build IS NULL AND id_entrepot_build IS NULL AND id_centre IS NULL AND id_construction IS NULL AND id_habitant = (SELECT id_habitant FROM habitant, village, maison WHERE village.id_user = 1 AND village.id_village = maison.id_village AND maison.id_maison = habitant.id_maison ORDER BY id_centre DESC LIMIT 1);"
                execute(sql, { })
                sql = "UPDATE centre SET nb_employee = nb_employee + 1 WHERE id_centre = " + str(res[i][0])
                execute(sql, { })
                return 'Ajout d\'un travailleur'
            except:
                return 'foo'
    return 'Il n\'y a pas de place dans ce type d\'usine'
        
def removeWork(ferme):
    sql = "SELECT id_centre, nb_employee FROM centre, village WHERE centre.enconstruction = false AND village.id_user = 1 AND village.id_village = centre.id_village AND centre.type_usine = '" + ferme + "';"
    res = execute(sql, { })
    for i in range (len(res)):
        if res[i][1] != 0:
            sql = "SELECT id_habitant FROM habitant, maison, village WHERE village.id_user = 1 AND  village.id_village = maison.id_village AND maison.id_maison = habitant.id_maison AND habitant.id_centre = " + str(res[i][0])
            id_hab = execute(sql, { })
            if len(id_hab) != 0:
                sql = "UPDATE habitant SET id_centre = NULL WHERE id_habitant = (SELECT id_habitant FROM habitant WHERE id_centre = " + str(res[i][0]) + " LIMIT 1);"
                execute(sql, { })
                sql = "UPDATE centre SET nb_employee = nb_employee - 1 WHERE id_centre = " + str(res[i][0])
                execute(sql, { })
                return "Employée remove !"
        
    return "Il n\'y a aucun travailleur dans ce type d\'usine !"

def addCentre(usine, bool):
    if bool:
        sql = "SELECT id_centre from centre, village WHERE village.id_village = centre.id_village AND centre.enconstruction = true;"
        res = execute(sql, { })
        if len(res) != 0:
            response = jsonify({'message': 'Une usine est déjà en amélioration'})
            response.status_code = 400
            return response
        sql = "SELECT quantite, entrepot.id_entrepot FROM village, stock, ressources, entrepot WHERE (ressources.name_res = 'Bois' OR ressources.name_res = 'Pierre') AND ressources.id_ressources = stock.id_ressources AND stock.id_entrepot = entrepot.id_entrepot AND entrepot.id_village = village.id_village AND village.id_user = 1 ORDER BY name_res;"
        res = execute(sql, { })
        is_enough = False

        match usine:
            case "Ferme":
                if (res[0][0] >= 10):
                    is_enough = True
            case "Scierie":
                if (res[0][0] >= 10) and (res[1][0] >= 5):
                    is_enough = True
            case "Carrière":
                if (res[0][0] >= 10) and (res[1][0] >= 5):
                    is_enough = True
            case "Mine":
                if (res[0][0] >= 30) and (res[1][0] >= 30):
                    is_enough = True

        if is_enough:
            start_build = centre(usine, True, None)
            if start_build[0]:
                match usine:
                    case "Ferme":
                        sql = "UPDATE stock SET quantite = quantite - 10 WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(res[0][1]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Bois'));"
                        execute(sql, { })
                    case "Scierie":
                        sql = "UPDATE stock SET quantite = quantite - 10 WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(res[0][1]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Bois'));"
                        sql = "UPDATE stock SET quantite = quantite - 5 WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(res[0][1]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Pierre'));"
                        execute(sql, { })
                    case "Carrière":
                        sql = "UPDATE stock SET quantite = quantite - 10 WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(res[0][1]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Bois'));"
                        sql = "UPDATE stock SET quantite = quantite - 5 WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(res[0][1]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Pierre'));"                    
                        execute(sql, { })
                    case "Mine":
                        sql = "UPDATE stock SET quantite = quantite - 30 WHERE id_stock IN (SELECT id_stock FROM stock, ressources WHERE stock.id_entrepot = " + str(res[0][1]) + " AND stock.id_ressources = ressources.id_ressources AND (ressources.name_res = 'Bois' OR ressources.name_res = 'Pierre'));"
                        execute(sql, { })
            response = jsonify({'message': start_build[1]})
            response.status_code = start_build[2] 
            return response
        else:
            response = jsonify({'message': 'Pas les ressources necessaires !'})
            response.status_code = 400
            return response
    else:
        sql = "UPDATE centre SET enconstruction = false WHERE enconstruction = true AND id_centre = (SELECT id_centre FROM entrepot, village WHERE village.id_village = entrepot.id_village AND village.id_user = 1) RETURNING id_centre;"
        id = execute(sql, { })
        end = centre(None, False, id)
        return 'Done'