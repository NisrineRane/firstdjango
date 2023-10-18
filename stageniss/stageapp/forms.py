from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class AcquirerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    location = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class ExhibitorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    location = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    description = forms.CharField(widget=forms.Textarea)  # Champ description sous forme de texte multiligne

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class OwnerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    location = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')



# forms.py

from django import forms

class LoanRequestForm(forms.Form):
    loan_duration = forms.IntegerField(
        label='Durée du Prêt (en jours)',
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    start_date = forms.DateField(
        label='Date de début',
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    # Champ pour le motif du prêt
    loan_purpose = forms.CharField(
        label='Motif du Prêt',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Informations de contact
    contact_name = forms.CharField(
        label='Nom',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    contact_email = forms.EmailField(
        label='Adresse E-mail',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    contact_phone = forms.CharField(
        label='Numéro de Téléphone',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Conditions spéciales
    special_conditions = forms.CharField(
        label='Conditions Spéciales (facultatif)',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    # Champ pour téléverser une image d'œuvre d'art (facultatif)
    artwork_image = forms.ImageField(
        label='Image d\'Œuvre d\'Art (facultatif)',
        required=False,
    )


from .models import LoanRequest

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['artwork', 'requester']