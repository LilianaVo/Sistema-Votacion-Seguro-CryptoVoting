"""
URL configuration for voting_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from voting import views as voting_views # Importamos la carpeta views de la app voting

urlpatterns = [
    # 1. URL de Administración de Django
    path('admin/', admin.site.urls),

    # 2. RUTAS DE AUTENTICACIÓN PERSONALIZADAS
    path('login/', voting_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    
    # NUEVA RUTA DE REGISTRO
    path('register/', voting_views.register_view, name='register'), # <-- NUEVA RUTA
    
    # Incluimos el resto de las rutas de autenticación (ej. reseteo de contraseña)
    path('', include('django.contrib.auth.urls')), 

    # 3. Mapeo de la aplicación de Votación
    path('voting/', include('voting.urls')),
    
    # 4. RUTA RAÍZ (/)
    path('', voting_views.index_view, name='home'), # Manda a la portada
    
]