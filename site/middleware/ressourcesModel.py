from lib.init_bdd import con
from middleware.villageModel import village_data
import math
from middleware.personModel import remove_pers

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

def mange():
    village = village_data(1)
    data = village['stock']
    nourriture = data[3][1]
    habitant = village['nbhabitant'][0][0]
    if nourriture > (habitant * 10) :
        sql = "UPDATE stock SET quantite = " + str(truncate((nourriture - (habitant * 10)), 1)) + " WHERE (SELECT ressources.id_ressources FROM ressources WHERE ressources.name_res = 'Nourriture') = stock.id_ressources AND id_entrepot = (SELECT id_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1);"
        execute(sql, {})
        return "Success"
    else: 
        tmp = nourriture // 10
        sql = "UPDATE stock SET quantite = " + str(truncate((nourriture - (tmp * 10)), 1)) + " WHERE (SELECT ressources.id_ressources FROM ressources WHERE ressources.name_res = 'Nourriture') = stock.id_ressources AND id_entrepot = (SELECT id_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1);"
        execute(sql, {})
        remove_pers(math.ceil(habitant - tmp))
        return "Error " + str(habitant - tmp)

def truncate(n, decimals = 0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def update_ressources():
    village = village_data(1)
    data = village['stock']

    pierre = data[0][1]
    nourriture = data[1][1]
    fer = data[2][1]
    bois = data[3][1]

    sum_res = pierre + nourriture + fer + bois

    max = village['level_entre'][0][1]


    for i in range (len(village['factory'])):
        match (village['factory'][i][1]):
            case 'Mine':
                add_fer = truncate( ((village['factory'][i][0] * 100 / 5 / 100) * 2.5 * 10), 1)
            case 'Carrière':
                add_pierre = truncate((( village['factory'][i][0] * 100 / 3 / 100) * 5 * 10), 1)
            case 'Ferme':
                add_nourriture = truncate((( village['factory'][i][0] * 100 / 2 / 100) * 9 * 10), 1)
            case 'Scierie':
                add_bois = truncate( ((village['factory'][i][0] * 100 / 3 / 100) * 5 * 10), 1)

    sum_add = add_bois + add_fer + add_nourriture + add_pierre

    if (sum_add + sum_res) > max:
        if sum_res >= max:
            return "Success"
        else:
            tmp = max - sum_res
            add = 0
            i = 0
            map = [add_bois, add_fer, add_nourriture, add_pierre]
            while add != tmp and i != 4:
                if (add + map[i]) <= tmp :
                    add = add + map[i]
                else:
                    map[i] = tmp - add
                    add = tmp
                i = i+1
            try:
                map[i-1] = truncate(map[i-1], 1)
            except:
                pass
            for r in range(i, len(map)):
                map[r] = 0

            add_bois = map[0]
            add_fer = map[1]
            add_nourriture = map[2]
            add_pierre = map[3]
        
    sql = "UPDATE stock SET quantite = quantite + " + str(truncate(add_bois, 1)) + " WHERE (SELECT ressources.id_ressources FROM ressources WHERE ressources.name_res = 'Bois') = stock.id_ressources AND id_entrepot = (SELECT id_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1);"
    execute(sql, {})
    sql = "UPDATE stock SET quantite = quantite + " + str(truncate(add_nourriture, 1)) + " WHERE (SELECT ressources.id_ressources FROM ressources WHERE ressources.name_res = 'Nourriture') = stock.id_ressources AND id_entrepot = (SELECT id_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1);"
    execute(sql, {})
    sql = "UPDATE stock SET quantite = quantite + " + str(truncate(add_fer, 1)) + " WHERE (SELECT ressources.id_ressources FROM ressources WHERE ressources.name_res = 'Fer') = stock.id_ressources AND id_entrepot = (SELECT id_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1);"
    execute(sql, {})
    sql = "UPDATE stock SET quantite = quantite + " + str(truncate(add_pierre, 1)) + " WHERE (SELECT ressources.id_ressources FROM ressources WHERE ressources.name_res = 'Pierre') = stock.id_ressources AND id_entrepot = (SELECT id_entrepot FROM entrepot, village WHERE entrepot.id_village = village.id_village AND village.id_user = 1);"
    execute(sql, {})
    return "Success"