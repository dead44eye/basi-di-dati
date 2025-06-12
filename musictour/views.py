from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .models import (
    Luogo, Evento, Partecipante, Organizzatore,
    Prenotazione, Recensione
)
from .forms import RegistrazioneForm, EventoForm


# Home page
def home(request):
    return render(request, 'home.html')


# Registrazione utente
def register_view(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_partecipante = form.cleaned_data['is_partecipante']
            user.is_organizzatore = form.cleaned_data['is_organizzatore']
            user.save()

            if user.is_partecipante:
                Partecipante.objects.create(
                    utente=user,
                    nome=user.first_name,
                    cognome=user.last_name,
                    email=user.email,
                    password=user.password  # opzionale
                )

            if user.is_organizzatore:
                Organizzatore.objects.create(
                    utente=user,
                    nome=user.first_name,
                    cognome=user.last_name
                )

            login(request, user)

            if user.is_partecipante and user.is_organizzatore:
                return redirect('scegli_ruolo')
            elif user.is_partecipante:
                return redirect('eventi')
            elif user.is_organizzatore:
                return redirect('gestisci_eventi')
            else:
                return redirect('home')
    else:
        form = RegistrazioneForm()

    return render(request, 'register.html', {'form': form})


# Login utente
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            print(f"DEBUG: login utente {user.username} -> is_partecipante={user.is_partecipante}, is_organizzatore={user.is_organizzatore}")

            if user.is_partecipante and user.is_organizzatore:
                return redirect('scegli_ruolo')
            elif user.is_partecipante:
                return redirect('eventi')
            elif user.is_organizzatore:
                return redirect('gestisci_eventi')
            else:
                return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})




# Pagina eventi (per partecipanti)
@login_required
def eventi_view(request):
    eventi = Evento.objects.all()
    return render(request, 'eventi.html', {'eventi': eventi})


# Prenota un evento
@login_required
def prenota_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    partecipante = get_object_or_404(Partecipante, utente=request.user)

    if Prenotazione.objects.filter(evento=evento, partecipante=partecipante).exists():
        return render(request, 'prenotazione_duplicata.html')

    codice = get_random_string(10)
    Prenotazione.objects.create(
        evento=evento,
        partecipante=partecipante,
        codice_conferma=codice
    )
    return render(request, 'prenotazione_successo.html', {'evento': evento})


# Prenotazioni dell'utente
@login_required
def mie_prenotazioni(request):
    partecipante = get_object_or_404(Partecipante, utente=request.user)
    prenotazioni = Prenotazione.objects.filter(partecipante=partecipante).select_related('evento', 'evento__luogo')

    prenotazioni_list = []
    for pren in prenotazioni:
        evento = pren.evento
        gia_recensito = Recensione.objects.filter(evento=evento, partecipante=partecipante).exists()
        recensibile = not gia_recensito
        prenotazioni_list.append({
            'prenotazione': pren,
            'evento': evento,
            'recensibile': recensibile
        })

    return render(request, 'mie_prenotazioni.html', {'prenotazioni': prenotazioni_list})


# Disdici prenotazione
@login_required
def disdici_prenotazione(request, prenotazione_id):
    prenotazione = get_object_or_404(Prenotazione, id=prenotazione_id, partecipante__utente=request.user)
    prenotazione.delete()
    return redirect('mie_prenotazioni')


# Scrivi recensione
@login_required
def scrivi_recensione(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    partecipante = get_object_or_404(Partecipante, utente=request.user)

    if not Prenotazione.objects.filter(evento=evento, partecipante=partecipante).exists():
        return render(request, 'errore.html', {'messaggio': 'Devi prenotare prima di recensire.'})

    if Recensione.objects.filter(evento=evento, partecipante=partecipante).exists():
        return render(request, 'errore.html', {'messaggio': 'Hai già recensito questo evento.'})

    if request.method == 'POST':
        punteggio = int(request.POST.get('punteggio'))
        testo = request.POST.get('testo')

        Recensione.objects.create(
            evento=evento,
            partecipante=partecipante,
            punteggio=punteggio,
            testo=testo,
            data=timezone.now().date()
        )
        return redirect('mie_prenotazioni')

    return render(request, 'scrivi_recensione.html', {'evento': evento})


# Tutte le recensioni
@login_required
def tutte_recensioni(request):
    recensioni = Recensione.objects.select_related('evento', 'partecipante').order_by('-data')
    return render(request, 'tutte_recensioni.html', {'recensioni': recensioni})


# Chi siamo
def chi_siamo(request):
    return render(request, 'chi_siamo.html')


# Gestione eventi (organizzatore)
@login_required
def gestisci_eventi(request):
    if not request.user.is_organizzatore:
        return redirect('home')

    organizzatore = get_object_or_404(Organizzatore, utente=request.user)
    eventi = Evento.objects.filter(organizzatori=organizzatore)

    return render(request, 'organizzatore/gestisci_eventi.html', {'eventi': eventi})

from .models import Luogo
# Crea evento
@login_required
def crea_evento(request):
    if not request.user.is_organizzatore:
        return redirect('home')

    organizzatore = get_object_or_404(Organizzatore, utente=request.user)
    luoghi = Luogo.objects.all()
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            evento.organizzatori.add(organizzatore)
            return redirect('gestisci_eventi')
    else:
        form = EventoForm()

    return render(request, 'organizzatore/crea_evento.html', {'form': form, 'luoghi': luoghi})


# Modifica evento
@login_required
def modifica_evento(request, evento_id):
    if not request.user.is_organizzatore:
        return redirect('home')

    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('gestisci_eventi')
    else:
        form = EventoForm(instance=evento)

    return render(request, 'organizzatore/modifica_evento.html', {'form': form, 'evento': evento})


# Elimina evento
@login_required
def elimina_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
    return redirect('gestisci_eventi')


# Scelta del ruolo (se utente è sia partecipante che organizzatore)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Partecipante  # Assicurati sia importato

from .models import Partecipante
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Partecipante  # Assicurati di importarlo

from .models import Partecipante

from django.contrib.auth.decorators import login_required
from .models import Partecipante

from .models import Partecipante

@login_required
def scegli_ruolo_view(request):
    user = request.user

    # 🔧 FIX AUTOMATICO: Se esiste oggetto Partecipante ma is_partecipante è False → aggiorna
    if not user.is_partecipante:
        if Partecipante.objects.filter(utente=user).exists():
            user.is_partecipante = True
            user.save()

    # Ora ricontrolla il flusso
    if user.is_partecipante and not user.is_organizzatore:
        return redirect('eventi')

    if user.is_organizzatore:
        if request.method == 'POST':
            ruolo_scelto = request.POST.get('ruolo')
            if ruolo_scelto == 'organizzatore':
                return redirect('gestisci_eventi')
            elif ruolo_scelto == 'partecipante':
                if not Partecipante.objects.filter(utente=user).exists():
                    Partecipante.objects.create(
                        utente=user,
                        nome=user.first_name,
                        cognome=user.last_name,
                        email=user.email,
                        password=user.password
                    )
                    user.is_partecipante = True
                    user.save()
                return redirect('eventi')
        return render(request, 'scegli_ruolo.html')

    return redirect('home')

