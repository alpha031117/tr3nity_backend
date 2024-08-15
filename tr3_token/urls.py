from django.urls import path
from . import views

urlpatterns = [
    path('api_token', views.test_api_token_conn, name='test-api-token'),
    path('api_mint_token', views.topUp_token, name='topUp-token'),
    path('api_check_balance', views.check_balance_api, name='check-balance'),
    
    # path('api_transfer_token/<str:capacity_used>', views.transfer_token, name='transfer-token'),
    # path('api_transfer_owner', views.transfer_owner, name='transfer-owner'),
    # path('callback-handler', views.callback_handler, name='callback_handler'),
    # path('api_get_transaction_to/<str:wallet_address>', views.get_transaction_filter_to, name='get-transaction-to'),
    # path('api_get_transaction_from/<str:wallet_address>', views.get_transaction_filter_from, name='get-transaction-from'),
    # path('api_get_all_transaction/<str:wallet_address>', views.get_combined_transactions, name='get-all-transaction'),
]