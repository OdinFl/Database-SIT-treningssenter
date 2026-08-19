-- Brukstilfelle 1
-- Senter
INSERT INTO Senter VALUES (1, 'Dragvoll idrettssenter', 'Loholt allé 81');
INSERT INTO Senter VALUES (2, 'Øya treningssenter', 'Vangslundsgate 2');
INSERT INTO Senter VALUES (3, 'Gløshaugen Idrettsbygg', 'Chr. Fredriks gate 20');
INSERT INTO Senter VALUES (4, 'DMMH treningsrom', 'Thrond Nergaards veg 7');

-- Sal
INSERT INTO Sal VALUES (1, 1, 26);
INSERT INTO Sal VALUES (2, 1, 32);
INSERT INTO Sal VALUES (3, 1, 16);
INSERT INTO Sal VALUES (1, 2, 22);
INSERT INTO Sal VALUES (2, 2, 18);

-- Sykkel
INSERT INTO Sykkel VALUES (1, 1, 1, FALSE);
INSERT INTO Sykkel VALUES (2, 1, 1, TRUE);
INSERT INTO Sykkel VALUES (3, 1, 1, FALSE);
INSERT INTO Sykkel VALUES (1, 1, 2, FALSE);
INSERT INTO Sykkel VALUES (2, 1, 2, TRUE);
INSERT INTO Sykkel VALUES (3, 1, 2, FALSE);
INSERT INTO Sykkel VALUES (1, 1, 3, TRUE);
INSERT INTO Sykkel VALUES (2, 1, 3, FALSE);
INSERT INTO Sykkel VALUES (1, 2, 1, FALSE);
INSERT INTO Sykkel VALUES (2, 2, 1, TRUE);
INSERT INTO Sykkel VALUES (3, 2, 1, FALSE);
INSERT INTO Sykkel VALUES (1, 2, 2, FALSE);
INSERT INTO Sykkel VALUES (2, 2, 2, FALSE);
INSERT INTO Sykkel VALUES (3, 2, 2, TRUE);

-- Brukere
INSERT INTO Bruker VALUES (1, 'Jonny Bravo', 'johnny@stud.ntnu.no', '94512378');
INSERT INTO Bruker VALUES (2, 'Kari Nordmann', 'kari.nordmann@gmail.com', '98765432');
INSERT INTO Bruker VALUES (3, 'Ola Hansen', 'ola.hansen@stud.ntnu.no', '91234567');
INSERT INTO Bruker VALUES (4, 'Sofia Eriksen', 'sofia.eriksen@gmail.com', '47382910');
INSERT INTO Bruker VALUES (5, 'Magnus Berg', 'magnus.berg@stud.ntnu.no', '93847261');
INSERT INTO Bruker VALUES (6, 'Ingrid Dahl', 'ingrid.dahl@gmail.com', '90123456');
INSERT INTO Bruker VALUES (7, 'Tobias Lund', 'tobias.lund@stud.ntnu.no', '48291037');
INSERT INTO Bruker VALUES (8, 'Emilie Strand', 'emilie.strand@gmail.com', '92837465');
INSERT INTO Bruker VALUES (9, 'Henrik Moen', 'henrik.moen@stud.ntnu.no', '41293847');
INSERT INTO Bruker VALUES (10, 'Astrid Vold', 'astrid.vold@gmail.com', '99182736');
INSERT INTO Bruker VALUES (11, 'Sander Holm', 'sander.holm@stud.ntnu.no', '46372819');
INSERT INTO Bruker VALUES (12, 'Nora Bakke', 'nora.bakke@gmail.com', '93746251');
INSERT INTO Bruker VALUES (13, 'Erlend Kvam', 'erlend.kvam@stud.ntnu.no', '48163729');

-- Instruktor
INSERT INTO Instruktor VALUES (1, 'Lars');
INSERT INTO Instruktor VALUES (2, 'Marte');
INSERT INTO Instruktor VALUES (3, 'Jonas');
INSERT INTO Instruktor VALUES (4, 'Silje');
INSERT INTO Instruktor VALUES (5, 'Kristine');
INSERT INTO Instruktor VALUES (6, 'Torben');
INSERT INTO Instruktor VALUES (7, 'Anette');

-- Gruppeaktivitet
INSERT INTO Gruppeaktivitet VALUES (1, 'Spin 4x4', 'En forutsigbar intervalltime: 4 stående intervaller på 4 minutter hver, med ca 2 minutter aktiv pause mellom hvert drag. God oppvarming og nedsykling inkludert.', 45);
INSERT INTO Gruppeaktivitet VALUES (2, 'Spin45', 'En variert spinningtime med 2-3 arbeidsperioder som passer for alle. Perfekt for deg som er ny på spinning! Du styrer intensiteten selv, og vi bruker takta til å tråkke oss gjennom timen.', 45);
INSERT INTO Gruppeaktivitet VALUES (3, 'Spin 8x3', 'En forutsigbar intervalltime med 8 intervaller på 3 minutter hver, der du sitter og står annethvert drag. 90-120 sek pause mellom hvert intervall. God oppvarming og nedsykling inkludert.', 55);
INSERT INTO Gruppeaktivitet VALUES (4, 'Spin60', 'En variert spinningtime som er noe mer utfordrende enn Spin45 med lengre varighet og tidvis høyere tempo. Du styrer likevel intensiteten selv, og timen passer alle som liker å tråkke i takt! Timen inneholder 2-4 arbeidsperioder med variert løype.', 60);


-- Reservasjoner (reservasjon_id, senter_id, sal_nr, dato, fra_tid, til_tid)
-- Timer 16. mars
INSERT INTO Reservasjon VALUES (1, 2, 1, '2026-03-16', '07:00:00', '07:45:00');
INSERT INTO Reservasjon VALUES (2, 1, 3, '2026-03-16', '16:30:00', '17:15:00');
INSERT INTO Reservasjon VALUES (3, 2, 2, '2026-03-16', '16:30:00', '17:15:00');
INSERT INTO Reservasjon VALUES (4, 2, 2, '2026-03-16', '17:40:00', '18:35:00');
INSERT INTO Reservasjon VALUES (5, 2, 1, '2026-03-16', '19:00:00', '20:00:00');

-- Timer 17. mars
INSERT INTO Reservasjon VALUES (6, 2, 1, '2026-03-17', '07:00:00', '07:55:00');
INSERT INTO Reservasjon VALUES (7, 2, 1, '2026-03-17', '18:30:00', '19:30:00');
INSERT INTO Reservasjon VALUES (8, 2, 2, '2026-03-17', '19:45:00', '20:30:00');

-- Timer 18. mars
INSERT INTO Reservasjon VALUES (9, 2, 1, '2026-03-18', '16:15:00', '17:15:00');
INSERT INTO Reservasjon VALUES (10, 1, 1, '2026-03-18', '16:30:00', '17:15:00');
INSERT INTO Reservasjon VALUES (11, 2, 2, '2026-03-18', '17:30:00', '18:15:00');
INSERT INTO Reservasjon VALUES (12, 2, 2, '2026-03-18', '18:30:00', '19:15:00');
INSERT INTO Reservasjon VALUES (13, 2, 1, '2026-03-18', '19:30:00', '20:25:00');

-- Timer 19. mars
INSERT INTO Reservasjon VALUES (14, 2, 1, '2026-03-19', '07:30:00', '08:25:00');
INSERT INTO Reservasjon VALUES (15, 2, 2, '2026-03-19', '16:45:00', '17:30:00');
INSERT INTO Reservasjon VALUES (16, 2, 1, '2026-03-19', '17:45:00', '18:45:00');

-- Timer 20. mars
INSERT INTO Reservasjon VALUES (17, 2, 1, '2026-03-20', '06:30:00', '07:15:00');
INSERT INTO Reservasjon VALUES (18, 2, 2, '2026-03-20', '16:30:00', '17:25:00');

-- Timer 21. mars
INSERT INTO Reservasjon VALUES (19, 2, 1, '2026-03-21', '10:00:00', '11:00:00');
INSERT INTO Reservasjon VALUES (20, 2, 2, '2026-03-21', '12:00:00', '12:55:00');

-- Timer 22. mars
INSERT INTO Reservasjon VALUES (21, 2, 1, '2026-03-22', '12:15:00', '13:00:00');

-- Gruppetime (timer_id, aktivitet_id, instruktor_id, reservasjon_id)
INSERT INTO Gruppetime VALUES (1, 1, 1, 1);
INSERT INTO Gruppetime VALUES (2, 1, 3, 2);
INSERT INTO Gruppetime VALUES (3, 2, 7, 3);
INSERT INTO Gruppetime VALUES (4, 3, 2, 4);
INSERT INTO Gruppetime VALUES (5, 4, 4, 5);
INSERT INTO Gruppetime VALUES (6, 3, 5, 6);
INSERT INTO Gruppetime VALUES (7, 4, 1, 7);
INSERT INTO Gruppetime VALUES (8, 2, 2, 8);
INSERT INTO Gruppetime VALUES (9, 4, 3, 9);
INSERT INTO Gruppetime VALUES (10, 2, 7, 10);
INSERT INTO Gruppetime VALUES (11, 1, 6, 11);
INSERT INTO Gruppetime VALUES (12, 2, 4, 12);
INSERT INTO Gruppetime VALUES (13, 3, 3, 13);
INSERT INTO Gruppetime VALUES (14, 3, 1, 14);
INSERT INTO Gruppetime VALUES (15, 2, 2, 15);
INSERT INTO Gruppetime VALUES (16, 4, 3, 16);
INSERT INTO Gruppetime VALUES (17, 2, 4, 17);
INSERT INTO Gruppetime VALUES (18, 3, 5, 18);
INSERT INTO Gruppetime VALUES (19, 4, 6, 19);
INSERT INTO Gruppetime VALUES (20, 3, 7, 20);
INSERT INTO Gruppetime VALUES (21, 2, 1, 21);


-- Brukstilfelle 5

-- Reservasjoner for Jonny sine gruppetimer
INSERT INTO Reservasjon VALUES (101, 2, 1, '2026-01-07', '07:15:00', '08:15:00');
INSERT INTO Reservasjon VALUES (102, 1, 1, '2026-01-28', '14:30:00', '15:15:00');
INSERT INTO Reservasjon VALUES (103, 2, 2, '2026-02-03', '17:30:00', '18:15:00');
INSERT INTO Reservasjon VALUES (104, 2, 2, '2026-02-23', '18:30:00', '19:15:00');
INSERT INTO Reservasjon VALUES (105, 2, 1, '2026-03-07', '07:30:00', '08:25:00');

-- Gruppetimer for Jonny
INSERT INTO Gruppetime VALUES (101, 4, 2, 101);
INSERT INTO Gruppetime VALUES (102, 2, 5, 102);
INSERT INTO Gruppetime VALUES (103, 1, 1, 103);
INSERT INTO Gruppetime VALUES (104, 2, 7, 104);
INSERT INTO Gruppetime VALUES (105, 3, 3, 105);

-- Bookinger (bruker_id, time_id, booking_tid, venteliste_plassering, status) for Jonny
INSERT INTO Booking VALUES (1, 101, '2026-01-06 14:32:00', NULL, 'møtt');
INSERT INTO Booking VALUES (1, 102, '2026-01-26 23:22:00', NULL, 'avbestilt');
INSERT INTO Booking VALUES (1, 103, '2026-02-02 14:32:00', 12, 'påmeldt');
INSERT INTO Booking VALUES (1, 104, '2026-02-22 23:32:00', NULL, 'møtt');
INSERT INTO Booking VALUES (1, 105, '2026-03-05 23:32:00', NULL, 'ikke møtt');

-- Bookinger for andre brukere (3-13)
INSERT INTO Booking VALUES (3, 101, '2026-01-05 10:00:00', NULL, 'møtt');
INSERT INTO Booking VALUES (3, 103, '2026-02-01 09:15:00', NULL, 'møtt');
INSERT INTO Booking VALUES (3, 105, '2026-03-04 18:00:00', NULL, 'avbestilt');

INSERT INTO Booking VALUES (5, 102, '2026-01-25 16:45:00', NULL, 'møtt');
INSERT INTO Booking VALUES (5, 104, '2026-02-21 11:30:00', NULL, 'møtt');

INSERT INTO Booking VALUES (8, 101, '2026-01-06 08:00:00', NULL, 'møtt');
INSERT INTO Booking VALUES (8, 102, '2026-01-27 20:00:00', NULL, 'møtt');
INSERT INTO Booking VALUES (8, 103, '2026-02-02 17:00:00', NULL, 'møtt');
INSERT INTO Booking VALUES (8, 105, '2026-03-05 12:00:00', NULL, 'påmeldt');

INSERT INTO Booking VALUES (11, 103, '2026-02-01 13:00:00', NULL, 'møtt');
INSERT INTO Booking VALUES (11, 104, '2026-02-22 19:00:00', NULL, 'avbestilt');
INSERT INTO Booking VALUES (11, 105, '2026-03-04 21:00:00', NULL, 'møtt');