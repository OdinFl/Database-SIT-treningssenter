PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Idrettslagsgruppe_Reservasjon;
DROP TABLE IF EXISTS Medlemskap;
DROP TABLE IF EXISTS Sykkel;
DROP TABLE IF EXISTS Tredemolle;
DROP TABLE IF EXISTS Apningstid;
DROP TABLE IF EXISTS Bemanningstid;
DROP TABLE IF EXISTS Prikk;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Gruppetime;
DROP TABLE IF EXISTS Gruppeaktivitet;
DROP TABLE IF EXISTS Idrettslagsgruppe;
DROP TABLE IF EXISTS Idrettslag;
DROP TABLE IF EXISTS Reservasjon;
DROP TABLE IF EXISTS Senter_Fasilitet;
DROP TABLE IF EXISTS Fasilitet;
DROP TABLE IF EXISTS Sal;
DROP TABLE IF EXISTS Senter;
DROP TABLE IF EXISTS Instruktor;
DROP TABLE IF EXISTS Bruker;

CREATE TABLE Bruker (
    bruker_id INTEGER PRIMARY KEY,
    navn VARCHAR(50) NOT NULL,
    epost VARCHAR(100) UNIQUE NOT NULL,
    mobilnr VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE Instruktor (
    instruktor_id INTEGER PRIMARY KEY,
    fornavn VARCHAR(50) NOT NULL
);

CREATE TABLE Senter (
    senter_id INTEGER PRIMARY KEY,
    senter_navn VARCHAR(100) NOT NULL,
    addresse VARCHAR(200) NOT NULL
);

CREATE TABLE Sal (
    sal_nr INTEGER NOT NULL,
    senter_id INTEGER NOT NULL,
    kapasitet INTEGER NOT NULL CHECK (kapasitet > 0),
    PRIMARY KEY (sal_nr, senter_id),
    FOREIGN KEY (senter_id) REFERENCES Senter(senter_id) ON DELETE CASCADE
);

CREATE TABLE Fasilitet (
    fasilitet_navn VARCHAR(100),
    beskrivelse TEXT,
    PRIMARY KEY (fasilitet_navn)
);

CREATE TABLE Senter_Fasilitet (
    fasilitet_navn VARCHAR(100) NOT NULL,
    senter_id INTEGER NOT NULL,
    PRIMARY KEY (senter_id, fasilitet_navn),
    FOREIGN KEY (senter_id) REFERENCES Senter(senter_id) ON DELETE CASCADE,
    FOREIGN KEY (fasilitet_navn) REFERENCES Fasilitet(fasilitet_navn) ON DELETE CASCADE
);

CREATE TABLE Reservasjon (
    reservasjon_id INTEGER PRIMARY KEY,
    senter_id INTEGER NOT NULL,
    sal_nr INTEGER NOT NULL,
    dato DATE NOT NULL,
    fra_tid TIME NOT NULL,
    til_tid TIME NOT NULL,
    FOREIGN KEY ( sal_nr, senter_id ) REFERENCES Sal(sal_nr, senter_id) ON DELETE CASCADE
);

CREATE TABLE Idrettslag (
    lag_id INTEGER PRIMARY KEY,
    navn VARCHAR(100) NOT NULL
);

CREATE TABLE Idrettslagsgruppe (
    gruppe_navn VARCHAR(100),
    lag_id INTEGER NOT NULL,
    PRIMARY KEY (lag_id, gruppe_navn),
    FOREIGN KEY (lag_id) REFERENCES Idrettslag(lag_id) ON DELETE CASCADE
);

CREATE TABLE Gruppeaktivitet (
    aktivitet_id INTEGER PRIMARY KEY,
    navn VARCHAR(50) NOT NULL,
    beskrivelse TEXT,
    varighet INTEGER NOT NULL
);

CREATE TABLE Gruppetime (
    time_id INTEGER PRIMARY KEY,
    aktivitet_id INTEGER NOT NULL,
    instruktor_id INTEGER NOT NULL,
    reservasjon_id INTEGER NOT NULL,
    FOREIGN KEY (aktivitet_id) REFERENCES Gruppeaktivitet(aktivitet_id) ON DELETE CASCADE,
    FOREIGN KEY (instruktor_id) REFERENCES Instruktor(instruktor_id) ON DELETE CASCADE,
    FOREIGN KEY (reservasjon_id) REFERENCES Reservasjon(reservasjon_id) ON DELETE CASCADE
);

CREATE TABLE Booking (
    bruker_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    booking_tid TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    venteliste_plassering INTEGER DEFAULT NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'påmeldt' CHECK (status IN ('påmeldt', 'møtt', 'ikke møtt', 'avbestilt')),
    PRIMARY KEY (bruker_id, time_id),
    FOREIGN KEY (bruker_id) REFERENCES Bruker(bruker_id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES Gruppetime(time_id) ON DELETE CASCADE
);

CREATE TABLE Prikk (
    prikk_id INTEGER,
    bruker_id INTEGER NOT NULL,
    utgår_dato DATETIME NOT NULL,
    PRIMARY KEY (prikk_id),
    FOREIGN KEY (bruker_id) REFERENCES Bruker(bruker_id) ON DELETE CASCADE
);

CREATE TABLE Bemanningstid (
    senter_id INTEGER NOT NULL,
    dag VARCHAR(10) NOT NULL CHECK (dag IN ('Mandag','Tirsdag','Onsdag','Torsdag','Fredag','Lørdag','Søndag')),
    fra_tid TIME NOT NULL,
    til_tid TIME NOT NULL,
    PRIMARY KEY (senter_id, dag, fra_tid),
    FOREIGN KEY (senter_id) REFERENCES Senter(senter_id) ON DELETE CASCADE,
    CONSTRAINT ck_bemanningstid CHECK (fra_tid < til_tid)
);

CREATE TABLE Apningstid (
    senter_id INTEGER NOT NULL,
    dag VARCHAR(10) NOT NULL CHECK (dag IN ('Mandag','Tirsdag','Onsdag','Torsdag','Fredag','Lørdag','Søndag')),
    apner TIME NOT NULL,
    stenger TIME NOT NULL,
    PRIMARY KEY (senter_id, dag, apner),
    FOREIGN KEY (senter_id) REFERENCES Senter(senter_id) ON DELETE CASCADE,
    CONSTRAINT ck_apningstid CHECK (apner < stenger)
);

CREATE TABLE Tredemolle (
    tredemolle_nr INTEGER NOT NULL,
    sal_nr INTEGER NOT NULL,
    senter_id INTEGER NOT NULL,
    produsent VARCHAR(100) NOT NULL,
    maks_hastighet REAL NOT NULL,
    maks_stigning REAL NOT NULL,
    PRIMARY KEY (tredemolle_nr, senter_id, sal_nr),
    FOREIGN KEY (sal_nr, senter_id) REFERENCES Sal(sal_nr, senter_id) ON DELETE CASCADE
);

CREATE TABLE Sykkel (
    sykkel_nr INTEGER NOT NULL,
    senter_id INTEGER NOT NULL,
    sal_nr INTEGER NOT NULL,
    bodybike BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (sykkel_nr, senter_id, sal_nr),
    FOREIGN KEY (sal_nr, senter_id) REFERENCES Sal(sal_nr, senter_id) ON DELETE CASCADE
);

CREATE TABLE Medlemskap (
    bruker_id INTEGER NOT NULL,
    lag_id INTEGER NOT NULL,
    PRIMARY KEY (bruker_id, lag_id),
    FOREIGN KEY (bruker_id) REFERENCES Bruker(bruker_id) ON DELETE CASCADE,
    FOREIGN KEY (lag_id) REFERENCES Idrettslag(lag_id) ON DELETE CASCADE
);

CREATE TABLE Idrettslagsgruppe_Reservasjon (
    lag_id INTEGER NOT NULL,
    gruppe_navn VARCHAR(100) NOT NULL,
    reservasjon_id INTEGER NOT NULL,
    PRIMARY KEY (lag_id, gruppe_navn, reservasjon_id),
    FOREIGN KEY (lag_id, gruppe_navn) REFERENCES Idrettslagsgruppe(lag_id, gruppe_navn),
    FOREIGN KEY (reservasjon_id) REFERENCES Reservasjon(reservasjon_id)

);