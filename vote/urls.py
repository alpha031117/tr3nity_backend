from django.urls import path
from . import views

urlpatterns = [
    # path('get-csrf-token', views.get_csrf_token, name='get_csrf_token'),

    path('vote', views.vote_project, name='vote_project'),
    path('get_all_projects', views.get_all_projects, name='get-all-projects'),
    path('get_projects/<str:reseacher_address>', views.get_projects, name='get-all-projects'),
]