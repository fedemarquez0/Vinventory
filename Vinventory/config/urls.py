"""vinventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from config import settings
from vinventory.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', custom_login, name='login'),
    path('signup/', custom_signup, name='signup'),
    path('logout/', custom_logout, name='logout'),

    path('', VinoList.as_view(), name='inicio'),
    path('vino/<int:codigo_vino>/', crear_vino, name='crearVino'),
    path('vino/<int:pk>', DetalleVino.as_view()),
    path('vino/update/<int:pk>/', VinoUpdate.as_view()),
    path('vino/delete/<int:pk>/', VinoDelete.as_view()),
    path('vino/decrementar/<int:vino_id>/', decrementar_stock, name='decrementar_stock'),
    path('vino/incrementar/<int:vino_id>/', incrementar_stock, name='incrementar_stock'),
    path('vino/verificar/', verificar_vino, name='verificar_vino'),

    path('bodega/', BodegaList.as_view(), name='verBodega'),
    path('bodega/create/', BodegaCreate.as_view()),
    path('bodega/update/<int:pk>/', BodegaUpdate.as_view()),
    path('bodega/delete/<int:pk>/', BodegaDelete.as_view()),

    path('origen/', OrigenList.as_view(), name='verOrigen'),
    path('origen/create/', OrigenCreate.as_view()),
    path('origen/update/<int:pk>/', OrigenUpdate.as_view()),
    path('origen/delete/<int:pk>/', OrigenDelete.as_view()),

    path('variedad/', VariedadList.as_view(), name='verVariedad'),
    path('variedad/create/', VariedadCreate.as_view()),
    path('variedad/update/<int:pk>/', VariedadUpdate.as_view()),
    path('variedad/delete/<int:pk>/', VariedadDelete.as_view()),

    path('estante/', EstanteList.as_view(), name='verEstantes'),
    path('estante/create/', EstanteCreate.as_view()),
    path('estante/update/<int:pk>/', EstanteUpdate.as_view()),
    path('estante/delete/<int:pk>/', EstanteDelete.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)