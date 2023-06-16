---- Création d'un utilisteur de test avec login = test2 et password = slt

INSERT INTO users (login, password) VALUES ('test2', '6d172a51caf9f698dbe5a79a654e60d466433407cfcf871dab50adb1abff7f3d646a510826f8ac1632fefd987a0c4401d4b061ed667dce8752cd93897bbacc9e');

INSERT INTO village (nom, nb_maison, id_user) VALUES ('village', 6, (SELECT id FROM users WHERE login = 'test2'));

INSERT INTO maison (nb_habitant, id_village, enconstruction) VALUES (2, 1, FALSE), (2, 1, FALSE), (2, 1, FALSE), (0, 1, FALSE), (0, 1, FALSE), (0, 1, FALSE);

INSERT INTO habitant (id_maison) VALUES (1), (1), (2), (2), (3), (3);

INSERT INTO entrepot (level_entrepot, capacite, id_village) VALUES (1, 300, 1);

INSERT INTO ressources (name_res) VALUES ('Bois'), ('Pierre'), ('Nourriture'), ('Fer');

INSERT INTO stock (id_ressources, id_entrepot, quantite) VALUES (1, 1, 20), (2, 1, 10), (3, 1, 50), (4, 1, 0);

INSERT INTO centre (nbmax, type_usine, production, id_village, enconstruction) VALUES (3, 'Scierie', 'Bois', 1, FALSE), (3, 'Carrière', 'Pierre', 1, FALSE), (2, 'Ferme', 'Nourriture', 1, FALSE), (5, 'Mine', 'Fer', 1, FALSE);