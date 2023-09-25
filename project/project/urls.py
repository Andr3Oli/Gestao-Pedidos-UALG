"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
    path('api-auth', include('rest_framework.urls')),
    path('api/', include('todo_api.urls')),
    path('funcionariomanager/', include(('funcionariomanager.urls', 'funcionariomanager'), namespace='funcionariomanager')),
    path('datamanager/', include(('datamanager.urls', 'datamanager'), namespace='datamanager')),
    path('requestmanager/', include(('requestmanager.urls', 'requestmanager'), namespace='requestmanager')),
    path('statmanager/', include(('statmanager.urls', 'statmanager'), namespace='statmanager')),
    path('authmanager/', include(('authmanager.urls', 'authmanager'), namespace='authmanager')),
    #path('utilizadores/', include(('utilizadores.urls', 'utilizadores'), namespace='utilizadores')),
    path('admin/', admin.site.urls),
]
