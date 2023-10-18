from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import *
from .models import *
import pdfkit
from django.template.loader import render_to_string
from django.http import FileResponse
from stageapp.models import LoanRequest



def account_choice(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')

        # En fonction du type de compte choisi, redirigez vers la page d'inscription appropriée
        if account_type == 'acquirer':
            return redirect('acquirer_signup')
        elif account_type == 'exhibitor':
            return redirect('exhibitor_signup')
        elif account_type == 'owner':
            return redirect('owner_signup')

    return render(request, 'account_choice.html')



def acquirer_signup(request):
    if request.method == 'POST':
        form = AcquirerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_acquirer = True
            user.save()
            login(request, user)
            return redirect('acquirer_dashboard')  # Redirigez vers le tableau de bord de l'acquéreur après l'inscription
    else:
        form = AcquirerSignUpForm()
    
    return render(request, 'acquirer_signup.html', {'form': form})



def exhibitor_signup(request):
    if request.method == 'POST':
        form = ExhibitorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_exhibitor  = True
            user.save()

            # Authentifiez et connectez l'utilisateur automatiquement après l'inscription
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)

            return redirect('exhibitor_dashboard')  # Redirigez vers le tableau de bord de l'acquéreur après l'inscription
    else:
        form = ExhibitorSignUpForm()
    return render(request, 'exhibitor_signup.html', {'form': form})



def owner_signup(request):
    if request.method == 'POST':
        form = OwnerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_owner   = True
            user.save()

            # Authentifiez et connectez l'utilisateur automatiquement après l'inscription
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)

            return redirect('owner_dashboard')  # Redirigez vers le tableau de bord de l'acquéreur après l'inscription
    else:
        form = OwnerSignUpForm()
    return render(request, 'owner_signup.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')  # Rediriger vers la page d'accueil ou une autre page



def login_view(request):
    error_message = None  # Initialisation du message d'erreur à None

    if request.method == 'POST':
        # Utilisation de request.POST.get() pour éviter les erreurs MultiValueDictKeyError
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentification de l'utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Connexion réussie
            login(request, user)

            # Redirection en fonction du type d'utilisateur
            if user.is_acquirer:
                return redirect('acquirer_dashboard')
            elif user.is_exhibitor:
                return redirect('exhibitor_dashboard')
            elif user.is_owner:
                return redirect('owner_dashboard')
        else:
            # Affichage d'un message d'erreur en cas d'échec de la connexion
            error_message = "Nom d'utilisateur ou mot de passe incorrect."

    return render(request, 'login_existing_user.html', {'error_message': error_message})



def home(request):
    return render(request, 'home_page.html')





def exhibitor_dashboard(request):
    # Votre code de vue pour le tableau de bord de l'exposant ici
    return render(request, 'exhibitor_dashboard.html')




def owner_dashboard(request):
    # Votre code de vue pour le tableau de bord du propriétaire ici
    return render(request, 'owner_dashboard.html')




def acquirer_dashboard(request):
    # Votre logique de vue pour le tableau de bord de l'acquéreur ici...
    return render(request, 'acquirer_dashboard.html')





def artwork_list(request):
    artworks = Artwork.objects.all()
    return render(request, 'artwork_list.html', {'artworks': artworks})





def create_loan_request(request, artwork_id):
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    
    if request.method == 'POST':
        loan_request = LoanRequest(artwork=artwork, requester=request.user)
        loan_request.save()
        messages.success(request, 'Votre demande de prêt a été soumise avec succès.')
        return redirect('artwork_list')
    
    return render(request, 'create_loan_request.html', {'artwork': artwork})




def artwork_list(request):
    artworks = Artwork.objects.all()
    return render(request, 'artwork_list.html', {'artworks': artworks})





def loan_requests(request):
    user = request.user
    requests = LoanRequest.objects.filter(requester=user)
    return render(request, 'loan_requests.html', {'requests': requests})





def loan_request_detail(request, request_id):
    loan_request = get_object_or_404(LoanRequest, pk=request_id)
    return render(request, 'loan_request_detail.html', {'loan_request': loan_request})





def respond_to_loan_request(request, request_id):
    loan_request = get_object_or_404(LoanRequest, pk=request_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            # Créez un contrat de prêt et marquez la demande comme acceptée
            contract = LoanContract(artwork=loan_request.artwork, lender=loan_request.artwork.owner, borrower=loan_request.requester)
            contract.save()
            loan_request.status = 'accepted'
            loan_request.save()
            messages.success(request, 'La demande de prêt a été acceptée.')
        elif action == 'reject':
            # Marquez la demande comme refusée
            loan_request.status = 'rejected'
            loan_request.save()
            messages.warning(request, 'La demande de prêt a été refusée.')

        return redirect('loan_requests')

    return render(request, 'respond_to_loan_request.html', {'loan_request': loan_request})






def loan_request_detail(request, request_id):
    loan_request = get_object_or_404(LoanRequest, pk=request_id)
    return render(request, 'loan_request_detail.html', {'loan_request': loan_request})




def respond_to_loan_request(request, request_id):
    loan_request = get_object_or_404(LoanRequest, pk=request_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            # Créez un contrat de prêt et marquez la demande comme acceptée
            contract = LoanContract(artwork=loan_request.artwork, lender=loan_request.artwork.owner, borrower=loan_request.requester)
            contract.save()

            # Générez le contenu du contrat en utilisant le modèle
            contract_content = render_to_string('loan_contract_template.html', {'contract': contract})

            # Enregistrez le contenu dans un fichier PDF
            contract_file_path = 'path_to_save_contract/loan_contract.pdf'
            with open(contract_file_path, 'w') as contract_file:
                contract_file.write(contract_content)

            # Enregistrez le chemin du fichier dans le modèle LoanContract
            contract.contract_file = contract_file_path
            contract.save()

            messages.success(request, 'La demande de prêt a été acceptée.')

            # Envoyez le contrat PDF au navigateur de l'emprunteur pour téléchargement
            with open(contract_file_path, 'rb') as pdf_file:
                response = FileResponse(pdf_file)
                response['Content-Disposition'] = 'attachment; filename="loan_contract.pdf"'
                return response
        elif action == 'reject':
            # Marquez la demande comme refusée
            loan_request.status = 'rejected'
            loan_request.save()
            messages.warning(request, 'La demande de prêt a été refusée.')

        return redirect('loan_requests')

    return render(request, 'respond_to_loan_request.html', {'loan_request': loan_request})





def demande_pret(request): 

    exhibitor = Exhibitor.objects.all()  # Move this line outside of the if block
    artworks = Artwork.objects.all()


    if request.method == "POST":
        # Get form data
        Artwork_id = request.POST.get('artwork')
        DateDebut = request.POST.get('DateDebut')
        HDebut = request.POST.get('HDebut')
        DateFin = request.POST.get('DateFin')
        HFin = request.POST.get('HFin')
        PJDemande = request.FILES.get('PJDemande')  # Change to FILES for file upload
        Exhibitor_id = request.POST.get('Exhibitor')

        # Get the Exhibitor object
        exhibitor_obj = User.objects.get(id=Exhibitor_id)  # Assuming User model is imported
        artwork_obj = Artwork.objects.get(id=Artwork_id)

        formatted_message = f"""
                <p><strong>Date Debut :</strong> {DateDebut}</p>
                <p><strong>Heure Debut :</strong> {HDebut}</p>
                <p><strong>Date Fin :</strong> {DateFin}</p>
                <p><strong>Heure Fin :</strong> {HFin}</p>
                <br />
                <p><strong>Objet :</strong>Demande Artwork {artwork_obj.title}</p>
                <br />
                Monsieur : <strong> {Exhibitor_id} </strong>
                <br />
                <p><strong>Message :</strong></p>
                <p>
                   J'aimerais vous demander si vous seriez d'accord pour prêter votre œuvre "{artwork_obj.title}" Durant la date : {DateDebut} {HDebut} jusqu'a {DateFin} {HFin}.
                </p>
                <br />
                Cordialement,
                <br /><br />
                
                <div style="font-family: Arial, sans-serif; color: #535353; font-size: 10pt;">
                    <p style="color: #2d4e77; font-weight: bold;">
                        PORTAIL Owner
                    </p>

                    <table style="border-collapse: collapse; width: 100%;">
                        <tr>
                            <td style="width: 225px; padding: 0 5.4pt;" valign="top">
                                <img width="154" height="43" src="http://s278824855.onlinehome.fr/images/logo.png" style="display: block;">
                            </td>
                            <td style="width: 413px; padding: 0 5.4pt;" valign="top">
                                <p style="font-weight: bold; color: #092800; line-height: 12.75pt;">
                                    INTELLCAP.
                                </p>
                                <p style="font-size: 8pt; font-weight: bold; color: #092800; line-height: 12.75pt;">
                                    Filiale de INTELLCAP PLC
                                </p>
                                <p style="font-size: 8.5pt; line-height: 12.75pt;">
                                    Hay Jedid | Rue Principale RN | 70050 Rabat 
                                </p>
                                <p style="font-size: 8.5pt; line-height: 12.75pt;">
                                    Mob 212 (0) xxx xxx xxx
                                </p>
                            </td>
                        </tr>
                    </table>

                    <p style="color: #1f497d; text-align: justify; line-height: 1.5;">
                        Cette communication et les pièces jointes sont destinées à la personne ou l'entité nommée ci-dessus et peuvent contenir des éléments confidentiels et / ou privilégiés. Toute révision, divulgation, diffusion, retransmission, publication ou toute autre utilisation ou prise de toute action sur la base de ces informations par des personnes ou entités autres que le destinataire est interdite. Si vous l'avez reçu par erreur, veuillez en informer 
                        l'expéditeur en répondant à cet e-mail ou par téléphone au +212 (0) 662 110 412 et enlevez le matériel de votre système. Les actions de INTELLCAP. et de ses employés sont régies par son code de conduite de manière éthique et en conformité avec toutes les lois anti-corruption et autres lois de chaque endroit où il est présent et en situation irrégulière doit être signalée sur le 
                        <a href="http://s278824855.onlinehome.fr/" target="_blank" style="color: #0056d6;">site web de la société</a> en toute confidentialité. INTELLCAP. est filiale de INTELLCAP Plc. INTELLCAP. au capital de 50 000 000 DH, RC Rabat N°18909, ICE N° 000333383000065 Patente N° 77612500, IF N° 18773131, Site aÌ Hay Jedid, Rue Principale SN - Rabat.
                    </p>

                    <p>
                        <a href="http://s278824855.onlinehome.fr/" target="_blank" style="color: #1f497d;">www.Intellcap.ma</a>
                    </p>
                    <p style="color: #00b050;">
                        Pensez à l'environnement avant d'imprimer cet e-mail.
                    </p>
                </div>

        """

        # Envoyer le mail
        send_mail(
            'Demande Artwork',
            '',  # Le corps du message est vide parce que nous utilisons html_message pour le contenu formaté en HTML
            exhibitor_obj.email,  # Ici, utilisez l'adresse e-mail de l'utilisateur comme expéditeur
            ['imanejadid16@gmail.com','nisrine.rane@usmba.ac.ma','Houss.benhassoun.1999@gmail.com'],  # Liste des destinataires
            # Utilisez l'argument html_message pour spécifier le contenu formaté en HTML
            html_message=formatted_message,
        )


        # Creating a new DemandePret object
        new_demande_pret = DemandePret(
            artwork=artwork_obj,
            DateDebut=DateDebut,
            HDebut=HDebut,
            DateFin=DateFin,
            HFin=HFin,
            PJDemande=PJDemande,
            Exhibitor=exhibitor_obj,  
        )

        # Saving the object to the database
        new_demande_pret.save()

        return redirect('demande_pret')

    return render(request, "create_loan_request.html", {'exhibitor': exhibitor, 'artworks': artworks})






"""

def my_view(request):
    # Autres opérations de vue

    # Ajoutez l'utilisateur connecté à votre contexte
    context = {'user': request.user}

    # Rendez votre modèle en incluant le contexte
    return render(request, 'acquirer_dashboard.html', context)

def my_view(request):
    # Autres opérations de vue

    # Ajoutez l'utilisateur connecté à votre contexte
    context = {'user': request.user}

    # Rendez votre modèle en incluant le contexte
    return render(request, 'owner_dashboard.html', context)

def my_view(request):
    # Autres opérations de vue

    # Ajoutez l'utilisateur connecté à votre contexte
    context = {'user': request.user}

    # Rendez votre modèle en incluant le contexte
    return render(request, 'exhibitor_dashboard.html', context)

"""



"""
def accept_loan_request(request, request_id):
    try:
        # Récupérez la demande de prêt avec l'ID request_id depuis la base de données
        loan_request = LoanRequest.objects.get(id=request_id)

        # Mettez en œuvre la logique d'acceptation ici
        # Par exemple, vous pourriez marquer la demande de prêt comme acceptée dans la base de données
        loan_request.status = 'accepted'
        loan_request.save()

        # Redirigez l'utilisateur vers la liste des demandes de prêt
        return redirect('loan_requests')

    except LoanRequest.DoesNotExist:
        # Gérez le cas où la demande de prêt n'existe pas
        return render(request, 'error.html', {'message': 'La demande de prêt spécifiée n\'existe pas.'})


def reject_loan_request(request, request_id):
    try:
        # Récupérez la demande de prêt avec l'ID request_id depuis la base de données
        loan_request = LoanRequest.objects.get(id=request_id)

        # Mettez en œuvre la logique de refus ici
        # Par exemple, vous pourriez marquer la demande de prêt comme refusée dans la base de données
        loan_request.status = 'rejected'
        loan_request.save()

        # Redirigez l'utilisateur vers la liste des demandes de prêt
        return redirect('loan_requests')

    except LoanRequest.DoesNotExist:
        # Gérez le cas où la demande de prêt n'existe pas
        return render(request, 'error.html', {'message': 'La demande de prêt spécifiée n\'existe pas.'})

"""



