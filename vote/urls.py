from django.urls import path
from . import views

urlpatterns = [
    # path('get-csrf-token', views.get_csrf_token, name='get_csrf_token'),

    path('vote/<int:project_id>/<str:validator_addrs>/<str:vote_choice>', views.vote_project, name='vote_project'),
]