from django.contrib.auth.models import AbstractUser
from django.db import models

class Utente(AbstractUser):
    is_partecipante = models.BooleanField(default=False)
    is_organizzatore = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({'P' if self.is_partecipante else ''}{'O' if self.is_organizzatore else ''})"

class Partecipante(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return str(self.utente)

class Organizzatore(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE)
    id_organizzatore = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)

    def __str__(self):
        return str(self.utente)


class Luogo(models.Model):
    nome = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=200)
    capienza = models.IntegerField()

class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateTimeField()
    descrizione = models.TextField()
    capienza = models.IntegerField()
    luogo = models.ForeignKey(Luogo, on_delete=models.CASCADE, null=True, blank=True)
    organizzatori = models.ManyToManyField(Organizzatore, through='Organizza', related_name='eventi_organizzati')

class Organizza(models.Model):
    organizzatore = models.ForeignKey(Organizzatore, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_organizzazione = models.DateField(null=True, blank=True)

class Prenotazione(models.Model):
    partecipante = models.ForeignKey(Partecipante, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_prenotazione = models.DateField(auto_now_add=True)
    codice_conferma = models.CharField(max_length=20)

class Recensione(models.Model):
    id_recensione = models.AutoField(primary_key=True)
    punteggio = models.IntegerField()
    data = models.DateField(auto_now_add=True)
    partecipante = models.ForeignKey(Partecipante, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    testo = models.TextField(null=True, blank=True)

class Scrive(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    recensione = models.OneToOneField(Recensione, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)

class Ubicazione(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    luogo = models.ForeignKey(Luogo, on_delete=models.CASCADE)
    orario_fine = models.TimeField(null=True, blank=True) 