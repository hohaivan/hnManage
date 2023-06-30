from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('dashboard/sale/', views.dashboard_sale, name='dashboard_sale'),
    path('dashboard/sale/live/', views.dashboard_sale, name='dashboard_sale_live'),
    path('dashboard/production/', views.dashboard_production, name='dashboard_production'),
    path('dashboard/production/live/', views.dashboard_production, name='dashboard_production_live'),
    path('dashboard/procurement/', views.dashboard_procure, name='dashboard_procure'),
    path('dashboard/procurement/live/', views.dashboard_procure, name='dashboard_procure_live'),
]