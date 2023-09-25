from django.urls import path
from authmanager.views import *


urlpatterns = [
    #path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("login/", login_action, name="login"),
    path('mensagem/<int:id>', mensagem,name='mensagem'),   
    
    path('escolher_perfil/', escolher_perfil, name='escolher_perfil'),
    path('register_user/<int:id>', criar_utilizador, name='register_user'),
    path('concluir_registo/<int:id>', concluir_registo, name='concluir_registo'),
    
    path('ajax/load-departamentos/', load_departamentos, name='ajax_load_departamentos'),
]
