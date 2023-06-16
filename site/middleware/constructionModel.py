from lib.init_bdd import con

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

def build_house(id_house, start):
    if start:
        sql = "SELECT id_habitant, village.nb_maison FROM habitant, maison, village WHERE id_entrepot_build IS NULL AND id_factory_build IS NULL AND id_construction IS NULL AND village.id_user = 1 AND village.id_village = maison.id_village AND maison.id_maison = habitant.id_maison;"
        res = execute(sql, { })

        if len(res) >= 2 :
            sql = "INSERT INTO maison (id_village, nb_habitant) VALUES ((SELECT id_village FROM village WHERE village.id_user = 1), 0) RETURNING id_maison;"
            id_house = execute(sql, { })
            sql = "UPDATE habitant SET id_construction = " + str(id_house[0][0]) + " WHERE id_habitant = " + str(res[0][0]) + " OR id_habitant = " + str(res[1][0])
            execute(sql, { })
            return True, 'Maison construite, elle sera disponible dans ' + str(60 + (res[0][1] - 6) * 15) + ' seconds', 201
        else:
            return False, 'Pas d\'habitant libre', 403
    else:
        sql = "UPDATE habitant SET id_construction = NULL WHERE id_construction = " + str(id_house)
        execute(sql, { })
        return 'Done'
    
def entrepot(id_entrepot, start, level):
    if start:
        sql = "SELECT id_habitant FROM habitant, maison, village WHERE habitant.id_construction IS NULL AND habitant.id_centre IS NULL AND habitant.id_factory_build IS NULL AND maison.id_maison = habitant.id_maison AND village.id_village = maison.id_village AND village.id_user = 1;"
        res = execute(sql, { })
        if len(res) < 3:
            return False, 'Pas d\'habitant libre', 403
        sql = "UPDATE habitant SET id_entrepot_build = " + str(id_entrepot) + " WHERE id_habitant = " + str(res[0][0]) + " OR id_habitant = " + str(res[1][0]) + " OR id_habitant = " + str(res[2][0])
        execute(sql, { })
        return True, 'Entrepot en amélioration, il sera pret dans ' + str(60 + (level[0][0] - 1) * 15) + ' seconds', 201
    else:
        sql = "UPDATE habitant SET id_entrepot_build = NULL WHERE id_entrepot_build = " + str(id_entrepot)
        execute(sql, { })
        return 'Done'

def centre(usine, start, id):
    if start:
        sql = "SELECT id_habitant FROM habitant, maison, village WHERE habitant.id_construction IS NULL AND habitant.id_centre IS NULL AND habitant.id_entrepot_build IS NULL AND habitant.id_factory_build IS NULL AND habitant.id_maison = maison.id_maison AND maison.id_village = village.id_village AND village.id_user = 1"
        res = execute(sql, { })
        is_enough = False
        nbmax = 0
        prod = None
        borne = 0
        match usine:
            case "Ferme":
                if len(res) >= 2:
                    is_enough = True
                    nbmax = 2
                    prod = "Nourriture"
                    borne = 2
            case "Scierie":
                if len(res) >= 3:
                    is_enough = True
                    nbmax = 3
                    prod = "Bois"
                    borne = 3
            case "Carrière":
                if len(res) >= 3:
                    is_enough = True
                    nbmax = 3
                    prod = "Pierre"
                    borne = 3
            case "Mine":
                if len(res) >= 5:
                    is_enough = True
                    nbmax = 5
                    prod = "Fer"
                    borne = 5
        if is_enough:
            sql = "INSERT INTO centre (id_village, nbmax, type_usine, production) VALUES ((SELECT id_village FROM village WHERE village.id_user = 1), " + str(nbmax) + ", '" + usine + "', '" + prod + "') RETURNING id_centre"
            id = execute(sql, { })
            sql = "UPDATE habitant SET id_factory_build = " + str(id[0][0]) + " WHERE id_habitant = " + str(res[0][0])
            tmp = ""
            for i in range (1, borne):
                tmp = tmp + " OR id_habitant = " + str(res[i][0])
            sql = sql + tmp
            execute(sql, { })
            return True, 'Centre en construction, il sera pret dans 60 seconds', 201, id
        else:
            return False, 'Pas d\'habitant libre', 403, None
    else: 
        sql = "UPDATE habitant SET id_factory_build = NULL WHERE id_factory_build = " + str(id[0][0])
        execute(sql, { })
        return 'Done'