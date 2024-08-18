from django.urls import path
from . import views

urlpatterns = [
    # path('get-csrf-token', views.get_csrf_token, name='get_csrf_token'),

    path('vote', views.vote_project, name='vote_project'),
    path('vote_count/<str:validator_address>', views.get_validator_vote_count, name='vote_count'),
    path('reputation_score/<str:validator_address>', views.get_validator_reputation_score, name='reputation_score'),
]