# 🎵 MusicTour - Portale per Eventi Musicali

MusicTour è una piattaforma web per partecipare o organizzare eventi musicali. Gli utenti possono registrarsi, prenotare eventi, crearli (se organizzatori) e lasciare recensioni.

---

##  Come usare il sito

### 1.  Home
- Pagina iniziale con collegamenti rapidi a tutte le sezioni (login, registrazione, eventi, prenotazioni, recensioni).
- Accessibile a tutti.

### 2.  Registrazione
- Inserisci username, password, email, nome e cognome.
- Seleziona se vuoi registrarti come **Partecipante**, **Organizzatore** o entrambi.
- I ruoli scelti determinano le funzionalità disponibili.

### 3.  Login
- Inserisci le credenziali registrate.
- Se sei sia partecipante che organizzatore, il sito ti chiederà con quale ruolo accedere.
- Verrai reindirizzato alla pagina eventi o alla gestione eventi in base alla tua scelta.

### 4.  Eventi
- Visualizza tutti gli eventi disponibili.
- Come partecipante puoi:
  - Vedere i dettagli degli eventi.
  - Prenotare un evento (una sola volta).
  - Disdire una prenotazione.
  - Scrivere una recensione solo dopo aver partecipato.

### 5.  Gestione Eventi
- Accessibile solo agli organizzatori.
- Crea un nuovo evento inserendo: nome, data, descrizione, capienza, luogo.
- Modifica o elimina gli eventi creati.

### 6.  Recensioni
- Dopo aver partecipato ad un evento, puoi lasciare una recensione con punteggio da 1 a 5 e un commento.
- Tutti gli utenti possono visualizzare le recensioni.

### 7.  Luoghi
- I luoghi vengono selezionati quando si crea un evento.
- Possono essere aggiunti tramite il pannello admin.

### 8.  Admin
- Accesso da `/admin`
- Richiede autenticazione superuser.
- Permette la gestione completa di utenti, eventi, recensioni, prenotazioni e luoghi.

---

##  Struttura del progetto

###  Modelli (models.py)
- **Utente** (custom): `username`, `password`, `email`, `is_partecipante`, `is_organizzatore`.
- **Partecipante**: `nome`, `cognome`, collegamento a `Utente`.
- **Organizzatore**: `nome`, `cognome`, collegamento a `Utente`.
- **Evento**: `nome`, `data`, `descrizione`, `capienza`, `luogo`, `organizzatore`.
- **Prenotazione**: `evento`, `partecipante`, `data_prenotazione`, `codice_conferma`.
- **Recensione**: `evento`, `partecipante`, `punteggio`, `testo`, `data`.
- **Luogo**: `nome`, `indirizzo`, `capienza`.

###  Viste (views.py)
- `register_view`
- `login_view`
- `scegli_ruolo_view`
- `eventi_view`
- `gestisci_eventi`
- `crea_evento`, `modifica_evento`, `elimina_evento`
- `prenota_evento`, `mie_prenotazioni`, `disdici_prenotazione`
- `scrivi_recensione`, `tutte_recensioni`
- `chi_siamo`, `home`

###  Template HTML
- `home.html`
- `register.html`
- `login.html`
- `eventi.html`
- `prenotazione_successo.html`
- `mie_prenotazioni.html`
- `scrivi_recensione.html`
- `tutte_recensioni.html`
- `organizzatore/gestisci_eventi.html`
- `organizzatore/crea_evento.html`
- `organizzatore/modifica_evento.html`
- `scegli_ruolo.html`

---

##  Avvio del progetto

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Visita il sito su:
 http://127.0.0.1:8000
________________________________________
Autore:
Francesco Ambrosio
Università degli Studi università degli studi di Napoli Parthenope
Corso: Basi di Dati 
