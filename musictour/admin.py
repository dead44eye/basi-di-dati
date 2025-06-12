from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utente, Partecipante, Organizzatore,
    Evento, Luogo, Organizza,
    Prenotazione, Recensione, Scrive, Ubicazione
)

@admin.register(Utente)
class UtenteAdmin(UserAdmin):
    model = Utente
    list_display = ['username', 'email', 'is_partecipante', 'is_organizzatore', 'is_staff']
    list_filter = ['is_partecipante', 'is_organizzatore', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_partecipante', 'is_organizzatore')}),
    )

admin.site.register(Partecipante)
admin.site.register(Organizzatore)
admin.site.register(Evento)
admin.site.register(Luogo)
admin.site.register(Organizza)
admin.site.register(Prenotazione)
admin.site.register(Recensione)
admin.site.register(Scrive)
admin.site.register(Ubicazione)
