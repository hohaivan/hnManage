from django.urls import path
from . import views

urlpatterns = [

    path('ledger_hn/<int:year>/', views.ledger_view_hn, name='ledger_view_hn'),
    path('ledger/<int:year>/', views.ledger_view, name='ledger_view'),
    path('ledger/add/', views.ledger_add, name='ledger_add'),
    path('ledger/delete/<int:pk>/', views.ledger_delete, name='ledger_delete'),
    path('ledger/update/<int:pk>/', views.ledger_update, name='ledger_update'),

    path('download/ledger/', views.export_ledger, name='ledger_export'),
    path('download/ledger/<int:year>', views.export_ledger, name='ledger_export'),
]