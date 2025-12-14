-- =========================
-- Table: VILLE
-- =========================
CREATE TABLE VILLE (
    Nom_Ville VARCHAR(100),
    Longitude DECIMAL(9,6),
    Latitude DECIMAL(9,6),
    Region VARCHAR(100),
    Pays VARCHAR(100),
    PRIMARY KEY (Nom_Ville)
);

-- =========================
-- Table: AGENCE_DE_VOYAGE
-- =========================
CREATE TABLE AGENCE_DE_VOYAGE (
    Cod_A INT,
    Site_web VARCHAR(200),
    Telephone VARCHAR(20),
    Adresse_Num_A VARCHAR(10),
    Adresse_Pays_A VARCHAR(100),
    Adresse_Rue_A VARCHAR(150),
    Adresse_Code_Postal VARCHAR(20),
    VILLE_Nom_Ville VARCHAR(100),
    PRIMARY KEY (Cod_A),
    FOREIGN KEY (VILLE_Nom_Ville) REFERENCES VILLE(Nom_Ville)
);

-- =========================
-- Table: CHAMBRE
-- =========================
CREATE TABLE CHAMBRE (
    Cod_C VARCHAR(20),
    Surface DECIMAL(6,2),
    PRIMARY KEY (Cod_C)
);

-- =========================
-- Table: SUITE (inheritance)
-- =========================
CREATE TABLE SUITE (
    CHAMBRE_Cod_C VARCHAR(20),
    PRIMARY KEY (CHAMBRE_Cod_C),
    FOREIGN KEY (CHAMBRE_Cod_C) REFERENCES CHAMBRE(Cod_C)
);

-- =========================
-- Table: HAS_ESPACES_DISPO
-- =========================
CREATE TABLE HAS_ESPACES_DISPO (
    ESPACES_DISPO_Espaces_Dispo VARCHAR(100),
    SUITE_CHAMBRE_Cod_C VARCHAR(20),
    PRIMARY KEY (ESPACES_DISPO_Espaces_Dispo, SUITE_CHAMBRE_Cod_C),
    FOREIGN KEY (SUITE_CHAMBRE_Cod_C) REFERENCES SUITE(CHAMBRE_Cod_C)
);

-- =========================
-- Table: HAS_EQUIPEMENT
-- =========================
CREATE TABLE HAS_EQUIPEMENT (
    CHAMBRE_Cod_C VARCHAR(20),
    EQUIPEMENT_Equipement VARCHAR(100),
    PRIMARY KEY (CHAMBRE_Cod_C, EQUIPEMENT_Equipement),
    FOREIGN KEY (CHAMBRE_Cod_C) REFERENCES CHAMBRE(Cod_C)
);

-- =========================
-- Table: RESERVATION
-- =========================
CREATE TABLE RESERVATION (
    CHAMBRE_Cod_C VARCHAR(20),
    Date_debut DATE,
    Date_fin DATE,
    Prix DECIMAL(10,2),
    AGENCE_DE_VOYAGE_Cod_A INT,
    PRIMARY KEY (CHAMBRE_Cod_C, Date_debut),
    FOREIGN KEY (CHAMBRE_Cod_C) REFERENCES CHAMBRE(Cod_C),
    FOREIGN KEY (AGENCE_DE_VOYAGE_Cod_A) REFERENCES AGENCE_DE_VOYAGE(Cod_A)
);
