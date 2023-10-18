
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User




class CustomUser(AbstractUser):
    is_acquirer = models.BooleanField(default=False)
    is_exhibitor = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    # Ajoutez les attributs related_name pour éviter les conflits avec les modèles User d'authentification
    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        related_query_name='custom_user',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
        related_query_name='custom_user',
        blank=True,
    )

class Acquirer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

class Exhibitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    description = models.TextField()  # Ajout du champ description


class Artwork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='static/assets/images/')
    price=models.IntegerField(default=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.title


class DemandePret(models.Model):
    IdDemandePret = models.AutoField(primary_key=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, null=True, default=None)
    DateDebut = models.DateField(null=True)
    HDebut = models.TimeField(null=True)
    DateFin = models.DateField(null=True)
    HFin = models.TimeField(null=True)
    PJDemande = models.TextField(null=True)
    Exhibitor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)


"""

class LoanContract(models.Model):
    
    lender = models.ForeignKey(User, related_name='lender_contracts', on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, related_name='borrower_contracts', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
     # Champ pour enregistrer le statut du contrat (approuvé, refusé, en attente, etc.)
    status = models.CharField(max_length=20, default='en_attente')  # Vous pouvez personnaliser les options de statut

    # Date et heure de création du contrat
    created_at = models.DateTimeField(auto_now_add=True)
    

"""


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    

class LoanRequest(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')