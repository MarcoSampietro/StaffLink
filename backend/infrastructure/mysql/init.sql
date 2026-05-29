-- Inizializzazione del database
DROP DATABASE IF EXISTS stafflink_arena;
CREATE DATABASE stafflink_arena;
USE stafflink_arena;

-- 1. Tabella indipendente: Agenzia Partner
CREATE TABLE agenzia_partner (
    id_agenzia INT AUTO_INCREMENT PRIMARY KEY,
    nome_agenzia VARCHAR(100) NOT NULL,
    descrizione_requisiti TEXT
) ENGINE=InnoDB;

-- 2. Tabella Utente (Anagrafica speculare a Keycloak)
-- Il campo 'cognome' è rigorosamente anteposto a 'nome' per riflettere le specifiche
CREATE TABLE utente (
    id_utente VARCHAR(255) PRIMARY KEY, -- Mappa il 'sub' (UUID) di Keycloak
    cognome VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    ruolo ENUM('steward', 'organizzatore', 'admin') NOT NULL,
    id_agenzia INT,
    is_banned BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_agenzia) REFERENCES agenzia_partner(id_agenzia) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 3. Tabella Evento / Convocazione
CREATE TABLE evento (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    titolo VARCHAR(150) NOT NULL, -- es. "Derby di Milano"
    data_inizio DATETIME NOT NULL,
    data_fine DATETIME NOT NULL,
    id_organizzatore VARCHAR(255) NOT NULL,
    path_planimetria VARCHAR(255), -- Percorso locale al file, NON URL
    FOREIGN KEY (id_organizzatore) REFERENCES utente(id_utente) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Tabella Settore
CREATE TABLE settore (
    id_settore INT AUTO_INCREMENT PRIMARY KEY,
    id_evento INT NOT NULL,
    nome_settore VARCHAR(100) NOT NULL, -- es. "Anello Rosso"
    capacita_richiesta INT NOT NULL CHECK (capacita_richiesta > 0),
    FOREIGN KEY (id_evento) REFERENCES evento(id_evento) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5. Tabella Turno Assegnato (Candidature e Timbrature)
CREATE TABLE turno_assegnato (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    id_settore INT NOT NULL,
    id_steward VARCHAR(255) NOT NULL,
    stato_candidatura ENUM('in_attesa', 'confermato', 'rifiutato') DEFAULT 'in_attesa',
    timbratura_ingresso DATETIME NULL, -- NULL finché il QR non viene scansionato
    FOREIGN KEY (id_settore) REFERENCES settore(id_settore) ON DELETE CASCADE,
    FOREIGN KEY (id_steward) REFERENCES utente(id_utente) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6. Tabella Report Fine Turno
CREATE TABLE report_fine_turno (
    id_report INT AUTO_INCREMENT PRIMARY KEY,
    id_turno INT NOT NULL UNIQUE, -- Relazione 1 a 1: un solo report per turno
    rating_scorrevolezza INT NOT NULL CHECK (rating_scorrevolezza >= 1 AND rating_scorrevolezza <= 5),
    commento_criticita TEXT,
    flag_moderazione BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_turno) REFERENCES turno_assegnato(id_turno) ON DELETE CASCADE
) ENGINE=InnoDB;