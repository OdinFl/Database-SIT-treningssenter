import os
import sqlite3
import datetime

"""
Oppretter database med schema
"""
def opprett_database(db_sti, schema_sti):
    con = sqlite3.connect(db_sti)

    with open(schema_sti, "r", encoding="utf-8") as f:
        schema = f.read()
    try:
        con.executescript(schema)
        con.commit()
        print(f"Database '{db_sti}' opprettet og initialisert med schema")
    except sqlite3.Error as e:
        print(f"Feil under initialisering: {e}")
        con.rollback()

    return con

"""
Kjører en sql fil
"""
def kjor_sql_file(con, sql_file):
    try:
        con.executescript(sql_file)
        con.commit()
        print("SQL file kjørt")
    except sqlite3.Error as e:
        print(f"Feil: {e}")
        con.rollback()


"""
Sletter databasen for slik at den kan bli bygget på nytt
""" 
def slett_db(db_sti):
    if os.path.exists(db_sti):
        os.remove(db_sti)
        print("Databasefil og alt innhold er slettet")
    else:
        print("Databasefilen eksisterer ikke")

"""
Beskrivelse: Gir ukeplanene for en bestemt uke, fra start-ukedag til søndag.
Bruker året som er akkurat nå, så hvis man kaller funksjonen i uke 52 av 2026 med ukedag=1,
så henter den informasjon fra 2026 (ikke 2027)
Input:
    - con: tilkoblingen til databasen
    - ukedag: ukedag som int der mandag er 1 og søndag er 7
    - uke_nummer: ukenummer
"""
def hent_ukeplan(con, uke_nummer):
    ar = datetime.datetime.now().year
    start_dato = datetime.date.fromisocalendar(ar, uke_nummer, 1)  # Mandag
    slutt_dato = datetime.date.fromisocalendar(ar, uke_nummer, 7)  # Søndag

    query = """
    SELECT  
        G.time_id,
        GA.navn AS aktivitet_navn,
        S.senter_navn,
        R.dato,
        R.fra_tid,
        R.til_tid
    FROM Gruppetime G
    JOIN Gruppeaktivitet GA ON G.aktivitet_id = GA.aktivitet_id
    JOIN Reservasjon R ON G.reservasjon_id = R.reservasjon_id
    JOIN Sal Sa ON R.sal_nr = Sa.sal_nr AND R.senter_id = Sa.senter_id
    JOIN Senter S ON Sa.senter_id = S.senter_id
    WHERE R.dato BETWEEN ? AND ?
    ORDER BY R.dato, R.fra_tid;
    """

    cursor = con.cursor()
    cursor.execute(query, (start_dato, slutt_dato))
    return cursor.fetchall()


def hent_bruker_fra_epost(con, epost):
    """
    Returnerer bruker_id til brukeren med gitt e-postadresse.
    Returnerer None hvis brukeren ikke finnes.
    """
    query = "SELECT bruker_id, navn FROM Bruker WHERE epost = ?"
    cursor = con.cursor()
    cursor.execute(query, (epost,))
    resultat = cursor.fetchone()
    if resultat:
        return resultat
    else:
        return None


def hent_bruker_historikk(con, epost, siden_ar):
    """
    Returnerer en liste av (time_id, senter_navn, dato, fra_tid, status) for alle bookinger
    til brukeren med gitt e-post, fra og med siden_ar.
    """
    query = """
    SELECT 
        B.time_id,
        S.senter_navn,
        R.dato,
        R.fra_tid,
        B.status
    FROM Booking B
    JOIN Bruker U ON B.bruker_id = U.bruker_id
    JOIN Gruppetime G ON B.time_id = G.time_id
    JOIN Reservasjon R ON G.reservasjon_id = R.reservasjon_id
    JOIN Sal Sa ON R.sal_nr = Sa.sal_nr AND R.senter_id = Sa.senter_id
    JOIN Senter S ON Sa.senter_id = S.senter_id
    WHERE U.epost = ?
      AND strftime('%Y', R.dato) >= ?
    ORDER BY R.dato, R.fra_tid;
    """
    cursor = con.cursor()
    cursor.execute(query, (epost, str(siden_ar)))
    return cursor.fetchall()

def sjekk_om_bruker_epost_eksisterer(con, epost):
    """
    Sjekker om en bruker med gitt e-post finnes i databasen.
    Returnerer True hvis brukeren finnes, ellers False.
    """
    query = "SELECT 1 FROM Bruker WHERE epost = ? LIMIT 1"
    cursor = con.cursor()
    cursor.execute(query, (epost,))
    return cursor.fetchone() is not None
    


"""
Beskrivelse: Finner time_id for en gruppetime basert på aktivitet_navn, dato, tid og senter_navn.
Output: Returnerer time_id hvis funnet, ellers None.
"""
def finn_gruppetime(con, aktivitet_navn, dato, tid, senter_navn):
    # Hent time_id
    query = """
    SELECT gt.time_id FROM Gruppetime gt
    JOIN Gruppeaktivitet ga ON gt.aktivitet_id = ga.aktivitet_id
    JOIN Reservasjon r ON gt.reservasjon_id = r.reservasjon_id
    JOIN Senter s ON r.senter_id = s.senter_id
    WHERE ga.navn = ? AND r.dato = ? AND r.fra_tid = ? AND s.senter_navn = ? 
    """
    time_id = con.execute(query, (aktivitet_navn, dato, tid, senter_navn)).fetchone()

    if not time_id:
        print(f"Ingen gruppetime funnet for {aktivitet_navn} på {dato} kl. {tid} ved {senter_navn}.")
        return None

    return time_id[0]

"""
Beskrivelse: Sjekker antall prikker for en bruker basert på bruker_id. 
Output: Returnerer antall gylige prikker (<=30 dager gamle)
"""
def sjekk_antall_prikker(con, bruker_id):
    dagens_dato = datetime.date.today().isoformat()
    query = """
    SELECT COUNT(*) 
    FROM Prikk WHERE bruker_id = ? AND utgår_dato>=?
    """
    prikker = con.execute(query, (bruker_id, dagens_dato)).fetchone()

    return prikker[0] if prikker else 0

"""
Beskrivelse: Sjekker om en bruker er svartelistet basert på antall prikker (>= 3)
Output: Returnerer True hvis brukeren har 3 eller flere prikker, ellers False
"""
def sjekk_svartliste(con, bruker_id):
    return sjekk_antall_prikker(con, bruker_id) >= 3


"""
Beskrivelse: Henter informasjon om timen
Input: time_id
Output: dato, fra_tid, til_tid, kapasitet, senter_navn, navn
"""
def hent_time_info(con, time_id):
    query = """
    SELECT r.dato,r.fra_tid,r.til_tid, sal.kapasitet, s.senter_navn, ga.navn 
    FROM Gruppetime gt JOIN Reservasjon r ON gt.reservasjon_id = r.reservasjon_id 
    JOIN Sal sal on r.sal_nr = sal.sal_nr AND r.senter_id = sal.senter_id 
    JOIN Senter s on r.senter_id = s.senter_id 
    JOIN Gruppeaktivitet ga on gt.aktivitet_id = ga.aktivitet_id WHERE gt.time_id = ?
    """
    return con.execute(query, (time_id,)).fetchone()


"""
Beskrivelse: Håndterer booking av trening for en bruker basert på bruker_id og time_id. 
Dersom sjekk_tid = True, så vil man ikke kunne booke mindre enn 5 min før trening.
Sjekker svarteliste, eksisterende booking, tid og kapasitet før booking.
Output: Returnerer True hvis booking er vellykket, ellers False.
"""
def booking_trening(con, bruker_id, time_id, sjekk_tid = False):
    # Sjekk om bruker er på svartelisten
    if sjekk_svartliste(con, bruker_id):
        print("Bruker har 3 eller flere prikker og er svartelistet. Kan ikke booke trening.")
        return False

    # Sjekk om brukeren allerede har booket den treningen
    status = None
    eksisterene_booking = con.execute("SELECT status FROM Booking WHERE bruker_id = ? AND time_id = ?", (bruker_id, time_id)).fetchone()
    if eksisterene_booking:
        status = eksisterene_booking[0]
        if status != "avbestilt":
            print("Bruker har allerede en booking for denne timen.")
            return False
    
    # Hent time info
    time_info = hent_time_info(con, time_id)

    # Sjekk om gruppetimen eksisterer
    if not time_info:
        print("Fant ingen informasjon for den angitte time_id.")
        return False

    dato, fra_tid, til_tid, kapasitet, senter_navn, aktivitet_navn = time_info

    # sjekk om booking er under 5 min før trening
    if sjekk_tid:
        start = datetime.datetime.fromisoformat(f"{dato} {fra_tid}")
        if datetime.datetime.now() > start - datetime.timedelta(minutes=5):
            print("Det er for sent å booke, fristen er 5 minutter før trening.")
            return False
    
    # Hent antall påmeldte
    pameldte = con.execute("""
        SELECT COUNT(*) FROM Booking
        WHERE time_id = ? AND venteliste_plassering IS NULL
    """, (time_id,)).fetchone()[0]

    # Hvis plass på trening så legg til bruker 
    if pameldte < kapasitet:
        # Legg til bruker i Booking
        if status == "avbestilt":
            con.execute("""UPDATE Booking 
                        SET status = ? 
                        WHERE bruker_id = ? 
                        AND time_id = ? """
                        ,("påmeldt", bruker_id, time_id))
        else:
            con.execute("""
                INSERT INTO Booking(bruker_id, time_id, status)
                VALUES (?, ?, 'påmeldt')
            """, (bruker_id, time_id))
            con.commit()

        print(f"Booking bekreftet! Du har fått plass! \n")
        return True

    else: # Hvis det ikke er plass på trening så legg til i venteliste

        # Hent neste plass i ventelista
        neste = con.execute("""
            SELECT COALESCE(MAX(venteliste_plassering), 0) + 1
            FROM Booking WHERE time_id = ?
        """, (time_id,)).fetchone()[0]

        # Legg til bruker i Booking, men på venteliste
        con.execute("""
            INSERT INTO Booking(bruker_id, time_id, venteliste_plassering, status)
            VALUES (?, ?, ?, 'påmeldt')
        """, (bruker_id, time_id, neste))
        con.commit()

        print(f"Timen er full. Du er på venteliste, plass nr. {neste}.")
        return True


    
"""
Beskrivelse: Registrerer oppmøte for en bruker basert på epost og time_id.
Oppdaterer status i Booking-tabellen til 'møtt' hvis oppmøte er registrert. 
"""
def registerer_oppmøte(con, epost ,time_id):
    # Hent bruker_id og time_id
    bruker = hent_bruker_fra_epost(con, epost)
    if not bruker:
        print(f"Bruker med epost {epost} finnes ikke.")
        return 

    bruker_id, navn = bruker

    con.execute(""" UPDATE Booking SET status = 'møtt' where bruker_id = ? and time_id = ?""", (bruker_id, time_id))
    con.commit()

    print(f"Oppmøte registrert for {navn} : {epost}. \n")

"""
Beskrivelse: Registrerer fravær for en time. Alle som er påmeldt,
men ikke markert som møtt vil få prikk og status 'ikke møtt'.
"""
def registerer_fravær(con, time_id):
    # finn alle som ikke har møtt opp
    ikke_mott = con.execute("""
        SELECT b.bruker_id, br.navn
        FROM Booking b
        JOIN Bruker br ON b.bruker_id = br.bruker_id
        WHERE b.time_id = ? AND b.status = 'påmeldt' AND b.venteliste_plassering IS NULL
    """, (time_id,)).fetchall()

    # Sjekk om listen er tom
    if not ikke_mott:
        print("Alle møtte opp.")
        return

    # Når prikken går ut
    utloper = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()

    # Oppdater til ikke møtt og gi prikk for hver bruker i ikke_mott
    for bruker_id, navn in ikke_mott:
        con.execute(
            "UPDATE Booking SET status = 'ikke møtt' WHERE bruker_id = ? AND time_id = ?",
            (bruker_id, time_id)
        )
        con.execute(
            "INSERT INTO Prikk(bruker_id, utgår_dato) VALUES (?, ?)",
            (bruker_id, utloper)
        )
        print(f"Prikk gitt til {navn}, (utløper {utloper}).")

    con.commit()


"""
Beskrivelse: Henter besøkshistorikk for en bruker basert på bruker_id og fra_dato.
Output: Returnerer en liste av tuples med aktivitet_navn, senter_navn, dato,
fra_tid og til_tid for alle timer brukeren har møtt opp på etter fra_dato.
"""
def hent_besokshistorikk(con, bruker_id, fra_dato):
    query = """
    SELECT DISTINCT ga.navn, s.senter_navn, r.dato, r.fra_tid, r.til_tid
    FROM Booking b
    JOIN Bruker br ON b.bruker_id = br.bruker_id
    JOIN Gruppetime gt ON b.time_id = gt.time_id
    JOIN Gruppeaktivitet ga ON gt.aktivitet_id = ga.aktivitet_id
    JOIN Reservasjon r ON gt.reservasjon_id = r.reservasjon_id
    JOIN Senter s ON r.senter_id = s.senter_id
    WHERE br.bruker_id = ? AND b.status = 'møtt' AND r.dato >= ?
    ORDER BY r.dato, r.fra_tid
    """

    return con.execute(query, (bruker_id, fra_dato)).fetchall()

"""
Beskrivelse: Henter informasjon om brukeren fra bruker_id
Input: bruker_id
Output: informasjon om brukeren fra Bruker
"""
def hent_bruker_fra_bruker_id(con, bruker_id):
    query = """
    SELECT *
    FROM Bruker
    WHERE bruker_id = ?
    """
    return con.execute(query, (bruker_id,)).fetchone()

"""
Beskrivelse: Skriver ut dato for når brukeren ikke lenger er på svartelisten.
Output: dato på eldste prikk om brukeren har prikker, eller None om ingen prikker.
"""
def svarteliste_utgar_dato(con, bruker_id):
    # Hent informasjon om brukeren
    bruker = hent_bruker_fra_bruker_id(con, bruker_id)
    if not bruker:
        print(f"Bruker med bruker_id '{bruker_id}' finnes ikke.")
        return

    idag = datetime.date.today()
    tretti_dager_siden = idag + datetime.timedelta(days=30)
    
    
    # Henter prikker som ikke har utgått
    prikker = con.execute("""
        SELECT utgår_dato FROM Prikk
        WHERE bruker_id  = ?
            AND utgår_dato >= ?
            AND utgår_dato <= ?
        ORDER BY utgår_dato""", (bruker_id, idag.isoformat(), tretti_dager_siden.isoformat())).fetchall()
    
    # Returner None om brukeren ikke har noen prikker eller færre prikker enn 3
    if not prikker or len(prikker) < 3:
        return None

    # returner eldste oprikk som utgår
    eldste_prikk = prikker[-1][0]
    return eldste_prikk
    
"""
Beskrivelse: Finner mest aktive brukere basert på antall møtt opp-timer i en gitt måned og år.
Output: Returnerer en liste av tuples med navn, epost og antall timer, sortert etter navn
"""
def mest_aktive_bruker(con, ar, maned):
    query = """
    WITH manedstrening AS (
        SELECT b.bruker_id, COUNT(*) AS antall
        FROM Booking b
        JOIN Gruppetime gt ON b.time_id = gt.time_id
        JOIN Reservasjon r ON gt.reservasjon_id = r.reservasjon_id
        WHERE b.status = 'møtt'
          AND strftime('%Y', r.dato) = ?
          AND strftime('%m', r.dato) = ?
        GROUP BY b.bruker_id
    )
    SELECT br.navn, br.epost, m.antall
    FROM manedstrening m
    JOIN Bruker br ON m.bruker_id = br.bruker_id
    WHERE m.antall = (SELECT MAX(antall) FROM manedstrening)
    ORDER BY br.navn
    """
    return con.execute(query, (str(ar), f"{maned:02d}")).fetchall()

def hent_aktiviteter(con):
    query = """SELECT ga.navn 
        FROM Gruppetime gt 
        JOIN Gruppeaktivitet ga ON gt.aktivitet_id = ga.aktivitet_id
        """
    resultater = con.execute(query).fetchall()
    return [rad[0] for rad in resultater]

def hent_bookinger(con, bruker_id):
    query = """SELECT gt.time_id, ga.navn, r.dato, r.fra_tid
        FROM Gruppetime gt
        JOIN Gruppeaktivitet ga ON gt.aktivitet_id = ga.aktivitet_id
        JOIN Reservasjon r ON r.reservasjon_id = gt.reservasjon_id
        JOIN Booking b ON gt.time_id = b.time_id
        WHERE b.bruker_id = ?
        AND b.status = 'påmeldt'"""

    resultater = con.execute(query, (bruker_id,)).fetchall()
    return resultater

def hent_navn_pa_aktiviteter(con):
    query = """SELECT aktivitet_id, navn
        FROM Gruppeaktivitet"""

    results = con.execute(query,).fetchall()
    return results


def hent_dato_pa_aktiviteter(con, aktivitet_id):
    query = """SELECT gt.time_id, r.dato, r.fra_tid, s.senter_navn
        FROM Gruppetime gt
        JOIN Gruppeaktivitet ga ON gt.aktivitet_id = ga.aktivitet_id
        JOIN Reservasjon r ON r.reservasjon_id = gt.reservasjon_id
        JOIN Senter s ON r.senter_id = s.senter_id
        WHERE ga.aktivitet_id = ?"""

    results = con.execute(query, (aktivitet_id,)).fetchall()
    return results



"""
Beskrivelse: Finner treningspartnere basert på antall felles møtt opp timer.
Output: Returnerer en liste av tuples med student_1, student_2 og antall felles timer, 
sortert etter antall felles timer i synkende rekkefølge.
"""
def finn_treningspar(con):
    query = """
    SELECT b1.epost, b2.epost, COUNT(*) AS antall_felles
    FROM Booking bk1
    JOIN Booking bk2 ON bk1.time_id = bk2.time_id AND bk1.bruker_id < bk2.bruker_id
    JOIN Bruker b1 ON bk1.bruker_id = b1.bruker_id
    JOIN Bruker b2 ON bk2.bruker_id = b2.bruker_id
    WHERE bk1.status = 'møtt' AND bk2.status = 'møtt'
    GROUP BY bk1.bruker_id, bk2.bruker_id
    ORDER BY antall_felles DESC
    """

    return con.execute(query).fetchmany(3)
