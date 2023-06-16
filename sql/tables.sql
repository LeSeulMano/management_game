CREATE TABLE users(
    id serial PRIMARY KEY,
    login VARCHAR(255),
    password VARCHAR(255),
    token VARCHAR(255)
);

CREATE TABLE village(
    id_village serial PRIMARY KEY,
    nom VARCHAR(50),
    nb_maison INT,
    id_user INT REFERENCES users(id),
    timer VARCHAR(6) DEFAULT '000000'
);

CREATE TABLE centre(
    id_centre serial PRIMARY KEY,
    nb_employee INT DEFAULT 0,
    nbmax INT,
    type_usine VARCHAR(8),
    production VARCHAR(10),
    id_village INT REFERENCES village(id_village),
    enconstruction BOOLEAN DEFAULT TRUE
);

CREATE TABLE entrepot(
    id_entrepot serial PRIMARY key,
    level_entrepot INT,
    capacite INT,
    id_village INT REFERENCES village(id_village),
    enconstruction BOOLEAN DEFAULT FALSE
);

CREATE TABLE ressources(
    id_ressources serial PRIMARY KEY,
    name_res VARCHAR(10)
);

CREATE TABLE stock(
    id_stock serial PRIMARY KEY,
    id_entrepot INT REFERENCES entrepot(id_entrepot),
    id_ressources INT REFERENCES ressources(id_ressources),
    quantite FLOAT
);

CREATE TABLE maison(
    id_maison serial PRIMARY KEY,
    nb_habitant INT DEFAULT 0,
    id_village INT REFERENCES village(id_village),
    enconstruction BOOLEAN DEFAULT TRUE
);

CREATE TABLE habitant(
    id_habitant serial PRIMARY KEY,
    id_maison INT REFERENCES maison(id_maison),
    id_centre INT REFERENCES centre(id_centre) DEFAULT NULL,
    id_construction INT REFERENCES maison(id_maison) DEFAULT NULL,
    id_entrepot_build INT REFERENCES entrepot(id_entrepot) DEFAULT NULL,
    id_factory_build INT REFERENCES centre(id_centre) DEFAULT NULL
);