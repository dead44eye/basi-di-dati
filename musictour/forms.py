from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utente, Evento


class RegistrazioneForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="Nome", required=True)
    last_name = forms.CharField(max_length=100, label="Cognome", required=True)
    email = forms.EmailField(label="Email", required=True)

    is_partecipante = forms.BooleanField(
        required=False,
        label="Registrati come Partecipante"
    )
    is_organizzatore = forms.BooleanField(
        required=False,
        label="Registrati come Organizzatore"
    )

    class Meta:
        model = Utente
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'is_partecipante',
            'is_organizzatore'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.is_partecipante = self.cleaned_data.get('is_partecipante', False)
        user.is_organizzatore = self.cleaned_data.get('is_organizzatore', False)

        if commit:
            user.save()
        return user


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'descrizione', 'data', 'capienza', 'luogo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'nome': 'Nome Evento',
            'descrizione': 'Descrizione',
            'data': 'Data',
            'luogo': 'Luogo'
        }