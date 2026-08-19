import functions as func
import re
import datetime

"""
Beskrivelse: Startmeny med alternativer
"""
def vis_meny():
    print("Skriv et av følgende valg:")
    print("Book trening:            book")
    print("Registrer oppmøte:       registrer")
    print("Vis ukeplan:             ukeplan")
    print("Vis besøkshistorikk:     historikk")
    print("Vis svarteliste:         svarteliste")
    print("Vis poengtavle:          poengtavle")
    print("Vis felles treninger:    felles")
    print("Brukertilfelle 6:        6")
    print("Avslutt program:         slutt") 


"""
Beskrivelse: Hent bruker input fra alternativer.
Dersom bruker input ikke matcher noen alternativer, så spør om ny input
Input: Alle mulige alternativer
Output: Bruker input
"""
def hent_bruker_input_fra_alternativer(mulige_alternativer):
    fortsett_input = True

    while fortsett_input:

        bruker_input = input("\n: ").lower()

        if bruker_input in mulige_alternativer:
            return bruker_input
        else:
            print("Forstod ikke kommando\nPrøv på nytt")


"""
Beskrivelse: Vis mulige alternativer til bruker
Input: type, de ulike alternativene.
Type vil si "Aktivitet" for alternatives: spin, løping
Output: 
"""
def vis_alternativer(type, alternativer):
    print(f"\nVelg {type}")
    print("Mulige alternativer: ")
    for alt in alternativer:
        print(alt)

"""
Beskrivelse: Hent ukenummer fra bruker. Må være et gyldig uke nummer
Output: Uke som int
"""
def hent_uke_nummer_fra_bruker():
    while True:
        print("Skriv inn uke nummer (1-52)")
        bruker_input = input("\n: ").strip()
        if bruker_input.lower() in ["q", "slutt"]:
            return None
        try:
            uke = int(bruker_input)
            if 1 <= uke <= 52:
                return uke
            else:
                print("Ukenummer må være mellom 1 og 52.")
        except ValueError:
            print("Skriv et gyldig tall mellom 1 og 52.")

"""
Beksrivelse: Hent email fra bruker. Må være gyldig format på mailen, 
og en bruker med den mailen må eksistere
output: email
"""
def hent_epost_fra_bruker(con):
    while True:
        print("Skriv inn e-postaddresse")
        epost = input("\n: ").strip()
        if epost.lower() in ["q", "slutt"]:
            return None

        # sjekk om epostaddresse er på format blank@blank.noe
        if not re.match(r"[^@]+@[^@]+\.[^@]+", epost):
            print("Skriv inn en gyldig e-postadresse eller 'slutt' for å avslutte.")
            continue

        # sjekk om brukeren eksisterer
        if not func.sjekk_om_bruker_epost_eksisterer(con, epost):
            print(f"Epost: {epost}, eksisterer ikke. Prøv på nytt eller skriv 'slutt' for å avslutte")
            continue
        return epost

"""
Beksrivelse: Hent år fra bruker. Må være mellom år 1900 og nå (2026)
Output: år som int
"""
def hent_ar_fra_bruker():
    ar = datetime.datetime.now().year
    while True:
        print("Skriv inn år")
        ar_input = input("\n: ").strip()
        if ar_input.lower() in ["q", "slutt"]:
            return None
        try:
            ar_input = int(ar_input)
            if 1900 <= ar_input <= ar:
                return ar_input
            else:
                print(f"Året må være mellom 1900 og {ar}")
        except ValueError:
            print("Skriv inn et gyldig årstall")

"""
Beskrivelse: Henter måned fra bruker. Må være mellom 1 og 12
Output: måned som int
"""
def hent_maned_fra_bruker():
    while True:
        print("Skriv inn måned")
        maned_input = input("\n: ").strip()
        if maned_input.lower() in ["q", "slutt"]:
            return None
        try:
            maned_input = int(maned_input)
            if 1 <= maned_input <= 12:
                return maned_input
            else:
                print(f"Månedne må være mellom 1 og 12")
        except ValueError:
            print("Skriv inn et gyldig måned")

"""
Beskrivelse: Stage weekplan. Spør bruker om ukenummer og ukedag.
Gir tilbake en ukeplan med alle aktiviteter for uka fra den ukedagen.
Vil sjekke for feil i bruker input.
Output: Neste stage
"""
def hent_ukeplan(con):
    valgt_uke = hent_uke_nummer_fra_bruker()
    if valgt_uke is None:
        return "q"

    ukeplan = func.hent_ukeplan(con, valgt_uke)

    # Lag en liste for hver ukedag (0=mandag, 6=søndag)
    aktiviteter_per_dag = [[] for _ in range(7)]
    for time_id, aktivitet, senter, dato, fra_tid, til_tid in ukeplan:
        ukedag = datetime.datetime.strptime(dato, "%Y-%m-%d").weekday()
        aktiviteter_per_dag[ukedag].append((time_id, aktivitet, senter, fra_tid, til_tid))

    ukedager = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    print(f"{'Ukedag':<10} {'Time-ID':<8} {'Aktivitet':<15} {'Senter':<22} {'Fra':<7} {'Til':<7}")
    print("-" * 75)
    for i, dag in enumerate(ukedager):
        if aktiviteter_per_dag[i]:
            for time_id, aktivitet, senter, fra_tid, til_tid in aktiviteter_per_dag[i]:
                print(f"{dag:<10} {time_id:<8} {aktivitet:<15} {senter:<22} {fra_tid:<7} {til_tid:<7}")
        else:
            print(f"{dag:<10} {'-':<8} {'-':<15} {'-':<22} {'-':<7} {'-':<7}")
    print()
    return "menu"

"""
Beskrivelse: Henter bruker historikk fra email og år.
Sjekker om bruker eksisterer og feil i input
Output: neste stage
"""
def fase_historikk(con):
    # Hent brukernavn
    epost = hent_epost_fra_bruker(con)
    if epost is None: # avslutt program
        return "q"

    # Hent år
    siden_ar = hent_ar_fra_bruker()
    if siden_ar is None: # avslutt program
        return "q"
    
    # Hent brukernavn fra database
    brukernavn = func.hent_bruker_fra_epost(con, epost)[1]

    # Hent historikk av bruker
    historikk = func.hent_bruker_historikk(con, epost, siden_ar)

    # Print på fint format
    print(f"Historikk for {brukernavn}")
    print(f"{'Time-ID':<8} {'Senter':<22} {'Dato':<10} {'Klokkeslett':<7} {'Status':<10}") # Irriterende at kolonner er flytta rart ved senter
    print("-" * 57)
    for rad in historikk:
        time_id, senter, dato, fra_tid, status = rad
        print(f"{time_id:<8} {senter:<22} {dato:<10} {fra_tid:<7} {status:<10}") # Irriterende at kolonner er flytta rart ved senter
    print()

    return "menu"

def fase_svarteliste(con):
    epost = hent_epost_fra_bruker(con)
    if epost is None:
        return "menu"

    bruker_id, navn = func.hent_bruker_fra_epost(con, epost)
    antall = func.sjekk_antall_prikker(con, bruker_id)
    if func.sjekk_svartliste(con, bruker_id):
        utgar = func.svarteliste_utgar_dato(con, bruker_id)
        print(f"\n{navn} er svartelistet med {antall} aktive prikker.")
        print(f"Svartelisten oppheves: {utgar}\n")
    else:
        print(f"\n{navn} er ikke svartelistet (har {antall} aktive prikker).\n")

    return "menu"

def registrer_oppmote(con):
    valgt_epost = hent_epost_fra_bruker(con)
    bruker_id = func.hent_bruker_fra_epost(con, valgt_epost)[0]

    aktivitet_rader = func.hent_bookinger(con, bruker_id)
    if len(aktivitet_rader) == 0:
        print('Denne brukeren har ingen aktive bookinger')
        print("\n")
        return "menu"

    aktivitet_ids = [str(rad[0]) for rad in aktivitet_rader]
    print("\nVelg gruppetime som skal registrere oppmøte")
    print(f"{'ID':<6} {'Navn':<15} {'Dato':<15} {'Fra tid'}")
    print("-" * 46)
    for rad in aktivitet_rader:
        print(f"{rad[0]:<6} {rad[1]:<15} {rad[2]:<15} {rad[3]}")

    valgt_aktivtet_id = hent_bruker_input_fra_alternativer(aktivitet_ids)
    func.registerer_oppmøte(con, valgt_epost, valgt_aktivtet_id)

    return "menu"

def book_gruppetime(con):
    valgt_epost = hent_epost_fra_bruker(con) # sjekker også om bruker eksisterer
    if valgt_epost is None: # Bruker vil avslutte programmet
        return "q"

    user_id = func.hent_bruker_fra_epost(con, valgt_epost)[0]

    aktiviteter = func.hent_navn_pa_aktiviteter(con)
    activitet_ider = [str(rad[0]) for rad in aktiviteter]

    print("\nVelg IDen til aktiviteten som du ønsker å booke")
    print(f"{'ID':<6} {'Navn':<10}")
    print("-" * 16)
    for rad in aktiviteter:
        print(f"{rad[0]:<6} {rad[1]:<10}")

    aktivitet_id = hent_bruker_input_fra_alternativer(activitet_ider)

    tidspunkter = func.hent_dato_pa_aktiviteter(con, aktivitet_id)
    gyldige_ider = [str(rad[0]) for rad in tidspunkter]

    print("\nVelg IDen til gruppetimen som du ønsker å booke")
    print(f"{'ID':<6} {'Dato':<15} {'Fra tid':<15} {'Treningssenter':<22}")
    print("-" * 58)
    for rad in tidspunkter:
        print(f"{rad[0]:<6} {rad[1]:<15} {rad[2]:<15} {rad[3]:<22}")

    valgt_gruppetime = hent_bruker_input_fra_alternativer(gyldige_ider)

    func.booking_trening(con, user_id, valgt_gruppetime)

    return "menu"


"""
Beskrivelse: Viser om en bruker er svartelistet og når svartelisten eventuelt oppheves.
"""
def fase_poengtavle(con):
    ar = hent_ar_fra_bruker()
    maned = hent_maned_fra_bruker()

    resultater = func.mest_aktive_bruker(con, ar, maned)

    if not resultater:
        print("Ingen treninger funnet for denne måneden.")
        return "menu"

    print(f"\nMest aktive brukere i {maned}/{ar}:")
    print(f"{'Navn':<20} {'Epost':<30} {'Antall'}")
    print("-" * 55)
    for navn, epost, antall in resultater:
        print(f"{navn:<20} {epost:<30} {antall}")

    print("\n")

    return "menu"

def fase_felles(con):
    resultater = func.finn_treningspar(con)

    if not resultater:
        print("Ingen felles treninger funnet.")
        return "menu"

    print("De 3 parene som har trent mest sammen")
    print("Bruker 1" + " " * 22 + "Bruker 2" + " " * 22 + "Felles treninger")
    print("-" * 70)
    for epost1, epost2, antall in resultater:
        print(f"{epost1:<30} {epost2:<30} {antall}")
    print("\n")

    return "menu"

"""
Beskrivelse: Hovedfunksjon for brukergrensesnitt.
Hver funksjon som brukeren vil gjøre er beskrevet som en fase.
Fasene er funksjoner som er definert i samme fil user_interface.py
"""
def grensesnitt(con):
    
    valgt_fase = "menu"

    while valgt_fase != "slutt" and valgt_fase != "q":
    
        if valgt_fase == "menu":
            vis_meny()     # Vis meny alternativer

            mulige_faser = ["slutt", "q", "book", "registrer", "ukeplan", "historikk", "svarteliste", "poengtavle", "felles","6"] # Alle mulige alternativer
            valgt_fase = hent_bruker_input_fra_alternativer(mulige_faser) # Håndter bruker input

        elif valgt_fase == "book":
            valgt_fase = book_gruppetime(con)

        elif valgt_fase == "registrer":
            valgt_fase = registrer_oppmote(con)

        elif valgt_fase == "ukeplan":
            valgt_fase = hent_ukeplan(con)

        elif valgt_fase == "historikk":
            valgt_fase = fase_historikk(con)

        elif valgt_fase == "svarteliste":
            valgt_fase = fase_svarteliste(con)

        elif valgt_fase == "poengtavle":
            valgt_fase = fase_poengtavle(con)

        elif valgt_fase == "felles":
            valgt_fase = fase_felles(con)

        elif valgt_fase == "6":
            valgt_fase = legg_til_brukertilfelle_prikker(con)
        
        

    print("Avslutter program")

"""
--- Brukertilfelle 6 ---
Beskrivelse: Legger til 3 prikker for Johnny. Prikkene utgår etter henholdsvis 25, 20 og 15 dager.
"""

def legg_til_brukertilfelle_prikker(con):
    # Hent dagens dato
    dagens_dato = datetime.date.today()

    # Legg til prikker med utløpsdatoer
    con.execute(
        "INSERT INTO Prikk(bruker_id, utgår_dato) VALUES (?, ?)",
        ( 1, (dagens_dato + datetime.timedelta(days=25)).isoformat())
    )
    con.execute(
        "INSERT INTO Prikk( bruker_id, utgår_dato) VALUES (?, ?)",
        ( 1, (dagens_dato + datetime.timedelta(days=13)).isoformat())
    )
    con.execute(
        "INSERT INTO Prikk(bruker_id, utgår_dato) VALUES (?, ?)",
        (1, (dagens_dato + datetime.timedelta(days=18)).isoformat())
    )

    print("3 prikker lagt til Johnny. Prikkene utgår etter henholdsvis 25, 13 og 18 dager.")
    return "menu"



