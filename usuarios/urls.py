from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('meseros/registro/', views.registro_mesero, name='registro_mesero'),
    path('meseros/lista/', views.lista_meseros, name='lista_meseros'),
]