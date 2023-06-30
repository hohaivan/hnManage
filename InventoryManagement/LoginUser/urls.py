from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='user-login'),
    path('changePW/', views.change_password, name='Change_Password')
]