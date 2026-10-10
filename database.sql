-- =========================================================
-- Gestion de parking : création de la base de données
-- À importer dans MySQL (par exemple avec phpMyAdmin dans XAMPP)
-- =========================================================

CREATE DATABASE IF NOT EXISTS gestion_parking
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE gestion_parking;

-- Une ligne par place de parking, avec la réservation en cours éventuelle
CREATE TABLE IF NOT EXISTS places_reservations (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    numero_place     VARCHAR(10)  NOT NULL,          -- V1…V20 (voitures), M1…M20 (motos)
    type_vehicule    VARCHAR(20)  NOT NULL,          -- Voiture ou Moto
    nom_utilisateur  VARCHAR(30)  DEFAULT NULL,
    date_reservation DATE         DEFAULT NULL,
    heure_debut      TIME         DEFAULT NULL,
    heure_fin        TIME         DEFAULT NULL,
    disponible       TINYINT(1)   DEFAULT 1          -- 1 = libre, 0 = occupée / réservée
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 20 places voitures (V1 à V20) et 20 places motos (M1 à M20)
INSERT INTO places_reservations (numero_place, type_vehicule) VALUES
    ('V1', 'Voiture'), ('V2', 'Voiture'), ('V3', 'Voiture'), ('V4', 'Voiture'), ('V5', 'Voiture'),
    ('V6', 'Voiture'), ('V7', 'Voiture'), ('V8', 'Voiture'), ('V9', 'Voiture'), ('V10', 'Voiture'),
    ('V11', 'Voiture'), ('V12', 'Voiture'), ('V13', 'Voiture'), ('V14', 'Voiture'), ('V15', 'Voiture'),
    ('V16', 'Voiture'), ('V17', 'Voiture'), ('V18', 'Voiture'), ('V19', 'Voiture'), ('V20', 'Voiture'),
    ('M1', 'Moto'), ('M2', 'Moto'), ('M3', 'Moto'), ('M4', 'Moto'), ('M5', 'Moto'),
    ('M6', 'Moto'), ('M7', 'Moto'), ('M8', 'Moto'), ('M9', 'Moto'), ('M10', 'Moto'),
    ('M11', 'Moto'), ('M12', 'Moto'), ('M13', 'Moto'), ('M14', 'Moto'), ('M15', 'Moto'),
    ('M16', 'Moto'), ('M17', 'Moto'), ('M18', 'Moto'), ('M19', 'Moto'), ('M20', 'Moto');
