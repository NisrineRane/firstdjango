from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # Autres URLS
    path('home/', home, name='home_page'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account_choice/', account_choice, name='account_choice'),
    path('acquirer_signup/', acquirer_signup, name='acquirer_signup'),
    path('exhibitor_signup/', exhibitor_signup, name='exhibitor_signup'),
    path('owner_signup/', owner_signup, name='owner_signup'),
    path('acquirer_dashboard/', acquirer_dashboard, name='acquirer_dashboard'),
    path('exhibitor_dashboard/', exhibitor_dashboard, name='exhibitor_dashboard'),
    path('owner_dashboard/', owner_dashboard, name='owner_dashboard'),



   #############################
    path('artworks/', artwork_list, name='artwork_list'),
    path('artworks/create_loan_request/', demande_pret, name='demande_pret'),
    #############################
    path('loan-requests/', loan_requests, name='loan_requests'),
    path('loan-requests/<int:request_id>/', loan_request_detail, name='loan_request_detail'),
    path('loan-requests/<int:request_id>/respond/', respond_to_loan_request, name='respond_to_loan_request'),

    #############   !!!!!   ################
    # path('accept_loan_request/<int:request_id>/', accept_loan_request, name='accept_loan_request'),
    # path('reject_loan_request/<int:request_id>/', reject_loan_request, name='reject_loan_request'),
    # path('some_path/', contract_template, name='contract_template'),
]
    
    # Autres URLS pour les autres types d'inscription
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

