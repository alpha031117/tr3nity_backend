from django.urls import path
from . import views

urlpatterns = [
    path('api_wallet', views.test_api_wallet_conn, name='test-api-token'),
    path('api_create_org_wallet', views.create_orgainsation_wallet, name='create-org-wallet'),
    path('api_create_user_wallet', views.create_user_wallet, name='create-user-wallet'),
    path('api_create_cat__wallet', views.create_wallet_category, name='create-wallet-category'),
    path('api_create_cat_entity', views.create_entity_category, name='create-entity-category'),
    path('api_create_entity', views.create_entity, name='create-entity'),

    path('api_get_entity', views.get_entity_list, name='get-entity'),
    path('api_get_cat_entity', views.get_cat_entity_list, name='get-cat-entity'),
    path('api_get_org_wallet', views.get_org_wallet_list, name='get-org-wallet'),
    path('api_get_user_wallet', views.get_user_wallet_list, name='get-user-wallet'),
    path('api_get_cat_wallet', views.get_cat_wallet, name='get-cat-wallet'),
    
    path('api_activate_wallet/', views.activate_wallet, name='activate-wallet'),
    path('api_deactivate_wallet/', views.deactivate_wallet, name='deactivate-wallet'),
    path('api_get_wallet_transaction/<str:address>/', views.get_wallet_transaction_count, name='get-wallet'),
]