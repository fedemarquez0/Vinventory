from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Vino, Bodega, Origen, Variedad, Estante

class VinoForm(forms.ModelForm):
    class Meta:
        model = Vino
        fields = '__all__'

class BodegaForm(forms.ModelForm):
    bodega = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la bodega'}))
    class Meta:
        model = Bodega
        fields = '__all__'

class OrigenForm(forms.ModelForm):
    origen = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del origen'}))
    class Meta:
        model = Origen
        fields = '__all__'

class VariedadForm(forms.ModelForm):
    variedad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la variedad'}))
    class Meta:
        model = Variedad
        fields = '__all__'

class EstanteForm(forms.ModelForm):
    estante = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del estante'}))
    class Meta:
        model = Estante
        fields = '__all__'

class VinoStockIncrementarForm(forms.Form):
    cantidad_a_incrementar = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad'}))

class VinoStockDecrementarForm(forms.Form):
    cantidad_a_decrementar = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad'}))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
