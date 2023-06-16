from lib.init_bdd import con
from middleware.villageModel import village_data


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

def remove_pers(nb):
    sql = "SELECT id_habitant, id_maison, id_centre FROM habitant GROUP BY id_habitant ORDER BY id_habitant DESC LIMIT " + str(nb - 1)
    res = execute(sql, { })
    try:
        sql = "DELETE FROM habitant WHERE CAST(id_habitant as integer) BETWEEN " + str(res[nb-1][0]) + " AND " + str(res[0][0]) +";"
        execute(sql, { })
        for i in range (len(res)):
            sql = "UPDATE maison SET nb_habitant = nb_habitant - 1 WHERE id_maison = " + str(res[i][1])
            execute(sql, { })
            sql = "UPDATE centre SET nb_employee = nb_employee - 1 WHERE id_centre = " + str(res[i][2])
            execute(sql, { })
        return 'ok'
    except:
        print("pas d'habitant")
        return 'pas d\'habitant'

def add_pers():
    sql = "SELECT id_maison FROM maison, village WHERE maison.nb_habitant < 2 AND maison.id_village = village.id_village AND village.id_user = 1 AND maison.enconstruction = false;"
    res = execute(sql, { })

    if len(res) == 0:
        return "Pas de maison disponible"
    
    sql =   "INSERT INTO habitant (id_maison) VALUES (" + str(res[0][0]) + ");";
    execute(sql, { })
    sql = "UPDATE maison SET nb_habitant = nb_habitant + 1 WHERE id_maison = " + str(res[0][0])
    execute(sql, { })
    return "Ajout d\'un habitant"
