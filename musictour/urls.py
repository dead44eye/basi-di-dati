from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import login_view, scegli_ruolo_view

urlpatterns = [
    # Home e autenticazione
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', login_view, name='login'),  # ✅ Usa la view personalizzata
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Eventi disponibili
    path('eventi/', views.eventi_view, name='eventi'),
    path('prenota/<int:evento_id>/', views.prenota_evento, name='prenota_evento'),

    # Prenotazioni personali
    path('mie-prenotazioni/', views.mie_prenotazioni, name='mie_prenotazioni'),
    path('disdici/<int:prenotazione_id>/', views.disdici_prenotazione, name='disdici_prenotazione'),

    # Recensioni
    path('recensisci/<int:evento_id>/', views.scrivi_recensione, name='scrivi_recensione'),
    path('recensioni/', views.tutte_recensioni, name='tutte_recensioni'),

    # Info
    path('chi-siamo/', views.chi_siamo, name='chi_siamo'),

    # Organizzatore - gestione eventi
    path('organizzatore/eventi/', views.gestisci_eventi, name='gestisci_eventi'),
    path('organizzatore/eventi/nuovo/', views.crea_evento, name='crea_evento'),
    path('organizzatore/eventi/modifica/<int:evento_id>/', views.modifica_evento, name='modifica_evento'),
    path('organizzatore/eventi/elimina/<int:evento_id>/', views.elimina_evento, name='elimina_evento'),

    # Scelta ruolo (per utenti con doppio ruolo)
    path('scegli-ruolo/', scegli_ruolo_view, name='scegli_ruolo'),
]
