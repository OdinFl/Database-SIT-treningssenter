# Database-SIT-treningssenter
Prosjekt til faget TDT4145  - Lagde et system for SIT treningssenter i Trondheim for å håndtere ulike brukstilfeller som medlemskap, arealer og påmeldinger.

### Hvordan bruke programmet som bruker

##### Start programmet
Åpne opp terminalen i prosjektmappen.
Åpne programmet: ```python src/main.py``` og kjør det


##### Tømme og Fylling av databasen
Programmet vil automatisk slette hele databasen før koden kjøres, før den vil laste inn alt av test data.


#### Brukertilfelle 1
Denne dataen er lagt inn i ```db/test_data.sql``` filen. Her legges det inn treningssenterene, saler, noen sykler i de ulike salene, brukere, trenere og treninger.


#### Brukertilfelle 2
For å få til brukertilfelle 2 så, må du ha kjørt  ```python src/main.py``` og da skal det komme opp en meny, her skal det først skrives inn `book`, så skiv inn mailen `johnny@stud.ntnu.no`. Så må du velge aktivitet og da skal du velge Spin60 som har id `4`, og da vil det komme opp når Spin60 gjennomføres og da skal du velge 17. mars kl 18.30 på Øya Treningssenter, den kommer til å ha id `7` og da vil bookingen bli bekreftet.

#### Brukertilfelle 3
Hvis du har allerede lagt inn en booking for Johnny som brukertilfelle 2 beskriver, kan du nå skrive inn `registrer`. Da skal du få opp en mulighet til å skrive inn mail til brukeren og da skal du skrive inn `johnny@stud.ntnu.no`. Her kommer du til å få opp alle bookingene til brukeren og vil da skrive inn gruppetime IDen som vil være `7`.

#### Brukertilfelle 4
I menyen kan du skrive `ukeplan` og her skal du skrive inn ukenummer som vil være `12`.

#### Brukertilfelle 5
For å få til brukertilfelle 5 må du skrive inn `historikk` i menyen og da må du skrive inn eposten til brukeren du ønsker å se, i vårt tilfelle vil dette være `johnny@stud.ntnu.no`. Så får du velge år som skal være `2026` og da skal det komme ut alle treningsøktene til Johnny i 2026.

#### Brukertilfelle 6
For å aktivere brukertilfelle 6, så må du kjøre ```python src/main.py``` og da skal du få en meny. Der kan du velge brukertilfelle 6 ved å skrive 6. Når du aktiverer brukertilfelle 6 vil det bli lagt til 3 prikker for `johnny@stud.ntnu.no`. Da vil du få opp en melding som bekrefter at prikkene har blitt lagt til. Da skal det ikke lenger være mulig for  `johnny@stud.ntnu.no` å booke noe mer.

#### Brukertilfelle 7
Brukertilfelle 7 kan sees ved å skrive inn `poengtavle` på menyen så vil du få valget om år og da skal du skrive inn `2026`. På måned må du skrive inn `1`, `2` eller `3` siden vi kun har hatt treningsøkter i disse månedene. Da vil du få ut den/de brukerne som har trent mest denne måneden.


#### Brukertilfelle 8
Brukertilfelle 8 kan sees ved å skrive inn `felles` i menyen, og da får du ut de tre parene som har flest treninger sammen. 
