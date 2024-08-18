from django.urls import path
from . import views

urlpatterns = [
    # path('get-csrf-token', views.get_csrf_token, name='get_csrf_token'),

    path('api_cert', views.test_api_cert_conn, name='test-api-cert'),
    path('api_cert_sm_list', views.get_cert_sm_list ,name='cert-sm-list'),
    path('api_cert_sm/<str:address>', views.get_cert_sm, name='cert-sm'),

    # path('api_mint_owner_cert/<str:researcher_address>/<str:project_name>/<str:project_description>', views.mint_cert_owner, name='mint-cert-owner'),
    path('research_upload', views.upload_research, name='research-upload'),
    path('research_published/<int:project_id>', views.publish_research, name='research-published'),
    path('api_mint_validator_cert', views.mint_cert_validator, name='mint-cert-validator'),
    path('api_mint_owner_cert/<str:researcher_address>/<str:project_name>/<str:project_description>', views.mint_cert_owner, name='mint-cert-owner'),

    path('api_get_owner_cert/<str:researcher_address>', views.get_owner_cert, name='get-cert-owner'),
    path('api_get_validator_cert/<str:validator_address>', views.get_validator_cert, name='get-validators'),
    path('api_get_pdf/<str:researcher_address>/<str:tokenID>', views.get_pdf_researcher, name='get-pdf'),
]