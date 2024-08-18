"""
URL configuration for tr3nity_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('tr3nity_token/', include('tr3_token.urls')),
    path('tr3nity_wallet/', include('tr3_wallet.urls')),
    path('tr3nity_certificate/', include('tr3_certificate.urls')),
    path('tr3nity_project/', include('vote_project.urls')),
    path('tr3nity_grants/', include('grants_project.urls')),
    path('admin/', admin.site.urls),
]