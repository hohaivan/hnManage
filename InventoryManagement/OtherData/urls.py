from django.urls import path
from . import views

urlpatterns = [
    path('data/Customer_info/', views.Customer_info, name='Customer_info'),
    path('data/Customer_info/add/', views.Customer_add, name='Customer_add'),
    path('data/Customer_info/delete/<int:pk>/', views.Customer_delete, name='Customer_delete'),
    path('data/Customer_info/update/<int:pk>/', views.Customer_update, name='Customer_update'),

    path('data/WH_OS/', views.WH_OS_ALL, name='WH_OS_ALL'),

    path('data/WH_OS/Weave', views.WH_KhoDet, name='WH_KhoDet'),
    path('data/WH_OS/Weave/add', views.WH_KhoDet_add, name='WH_KhoDet_add'),
    path('data/WH_OS/Weave/delete/<int:pk>/', views.WH_KhoDet_delete, name='WH_KhoDet_delete'),
    path('data/WH_OS/Weave/update/<int:pk>/', views.WH_KhoDet_update, name='WH_KhoDet_update'),

    path('data/WH_OS/Bleach', views.WH_KhoTay, name='WH_KhoTay'),
    path('data/WH_OS/Bleach/add', views.WH_KhoTay_add, name='WH_KhoTay_add'),
    path('data/WH_OS/Bleach/delete/<int:pk>/', views.WH_KhoTay_delete, name='WH_KhoTay_delete'),
    path('data/WH_OS/Bleach/update/<int:pk>/', views.WH_KhoTay_update, name='WH_KhoTay_update'),
    
    path('data/WH_OS/Print', views.WH_KhoIn, name='WH_KhoIn'),
    path('data/WH_OS/Print/add', views.WH_KhoIn_add, name='WH_KhoIn_add'),
    path('data/WH_OS/Print/delete/<int:pk>/', views.WH_KhoIn_delete, name='WH_KhoIn_delete'),
    path('data/WH_OS/Print/update/<int:pk>/', views.WH_KhoIn_update, name='WH_KhoIn_update'),
    
    path('data/WH_OS/Dye', views.WH_KhoNhuom, name='WH_KhoNhuom'),
    path('data/WH_OS/Dye/add', views.WH_KhoNhuom_add, name='WH_KhoNhuom_add'),
    path('data/WH_OS/Dye/delete/<int:pk>/', views.WH_KhoNhuom_delete, name='WH_KhoNhuom_delete'),
    path('data/WH_OS/Dye/update/<int:pk>/', views.WH_KhoNhuom_update, name='WH_KhoNhuom_update'),

    path('data/WH_OS/Stretch', views.WH_KhoCang, name='WH_KhoCang'),
    path('data/WH_OS/Stretch/add', views.WH_KhoCang_add, name='WH_KhoCang_add'),
    path('data/WH_OS/Stretch/delete/<int:pk>/', views.WH_KhoCang_delete, name='WH_KhoCang_delete'),
    path('data/WH_OS/Stretch/update/<int:pk>/', views.WH_KhoCang_update, name='WH_KhoCang_update'),

    path('data/WH_OS/ProductClass/', views.WH_ProductType, name='WH_ProductType'),
    path('data/WH_OS/ProductClass/delete/<int:pk>/', views.WH_ProductType_delete, name='WH_ProductType_delete'),
    path('data/WH_OS/ProductClass/update/<int:pk>/', views.WH_ProductType_update, name='WH_ProductType_update'),

    path('data/WH_OS/CungCapSoi/', views.WH_YarnVendor, name='WH_YarnVendor'),
    path('data/WH_OS/CungCapSoi/add', views.WH_YarnVendor_add, name='WH_YarnVendor_add'),
    path('data/WH_OS/CungCapSoi/delete/<int:pk>/', views.WH_YarnVendor_delete, name='WH_YarnVendor_delete'),
    path('data/WH_OS/CungCapSoi/update/<int:pk>/', views.WH_YarnVendor_update, name='WH_YarnVendor_update'),
    
    path('data/WH_OS/YarnWH/', views.WH_Warehouse, name='WH_Warehouse'),
    path('data/WH_OS/YarnWH/add', views.WH_Warehouse_add, name='WH_Warehouse_add'),
    path('data/WH_OS/YarnWH/delete/<int:pk>/', views.WH_Warehouse_delete, name='WH_Warehouse_delete'),
    path('data/WH_OS/YarnWH/update/<int:pk>/', views.WH_Warehouse_update, name='WH_Warehouse_update'),
    
    path('data/WH_OS/YarnType/', views.WH_YarnType, name='WH_YarnType'),
    path('data/WH_OS/YarnType/delete/<int:pk>/', views.WH_YarnType_delete, name='WH_YarnType_delete'),
    path('data/WH_OS/YarnType/update/<int:pk>/', views.WH_YarnType_update, name='WH_YarnType_update'),


]