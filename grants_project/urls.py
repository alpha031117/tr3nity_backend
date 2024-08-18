from django.urls import path
from . import views

urlpatterns = [
    path('get_all_projects', views.get_all_projects, name='get-all-projects'),
    path('get_project_by_id/<int:project_id>', views.get_project_by_id, name='get-project'),
    path('get_projects/<int:grant_id>', views.get_projects, name='get-projects'),
    path('get_all_grants', views.get_all_grants, name='get-all-grants'),
    path('get_grant/<int:grant_id>', views.get_grant, name='get-grant'),
    path('create_grant', views.create_grant, name='create-grant'),
]