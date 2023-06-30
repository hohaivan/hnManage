from django.urls import path
from . import views

urlpatterns = [
    path('yarn/order_hn/<int:year>/', views.order_hn, name='yarn_order_hn'),
    path('yarn/order/<int:year>/', views.order, name='yarn_order'),
    path('yarn/order/add/', views.order_add, name='yarn_order_add'),
    path('yarn/order/delete/<int:pk>/', views.order_delete, name='yarn_order_delete'),
    path('yarn/order/update/<int:pk>/', views.order_update, name='yarn_order_update'),

    path('yarn/delivery_hn/<int:year>/', views.delivery_hn, name='yarn_delivery_hn'),
    path('yarn/delivery/<int:year>/', views.delivery, name='yarn_delivery'),
    path('yarn/delivery/add/<int:pk>/', views.delivery_add, name='yarn_delivery_add'),
    path('yarn/delivery/delete/<int:pk>/', views.delivery_delete, name='yarn_delivery_delete'),
    path('yarn/delivery/update/<int:pk>/', views.delivery_update, name='yarn_delivery_update'),

    path('yarn/transfer_hn/<int:year>/', views.transfer_hn, name='yarn_transfer_hn'),
    path('yarn/transfer/<int:year>/', views.transfer, name='yarn_transfer'),
    path('yarn/transfer/add/', views.transfer_add, name='yarn_transfer_add'),
    path('yarn/transfer/delete/<int:pk>/', views.transfer_delete, name='yarn_transfer_delete'),
    path('yarn/transfer/update/<int:pk>/', views.transfer_update, name='yarn_transfer_update'),

    path('yarn/payment_hn/<int:year>', views.Yarn_Pay_hn, name='yarn_pay_hn'),
    path('yarn/payment/<int:year>', views.Yarn_Pay, name='yarn_pay'),
    path('yarn/payment/add/', views.Yarn_Pay_add, name='yarn_pay_add'),
    path('yarn/payment/delete/<int:pk>/', views.Yarn_Pay_delete, name='yarn_pay_delete'),
    path('yarn/payment/update/<int:pk>/', views.Yarn_Pay_update, name='yarn_pay_update'),

    path('yarn/debt/<int:year>', views.Yarn_Debt, name='yarn_debt'),
    path('yarn/debt/add/<int:Vendor_id>/<int:Year>', views.Yarn_Debt_add, name='yarn_debt_add'),
    path('yarn/debt/update/<int:Vendor_id>/<int:Year>', views.Yarn_Debt_update, name='yarn_debt_update'),

    path('download/DatSoi/', views.export_YarnOrder, name='YarnOrder_export'),
    path('download/DatSoi/<int:year>', views.export_YarnOrder, name='YarnOrder_export'),
    path('download/GiaoSoi/', views.export_Delivery, name='Delivery_export'),
    path('download/GiaoSoi/<int:year>', views.export_Delivery, name='Delivery_export'),
    path('download/XNSoi/', views.export_Transfer, name='Transfer_export'),
    path('download/XNSoi/<int:year>', views.export_Transfer, name='Transfer_export'),
    path('download/TraTienSoi/', views.export_YarnPay, name='YarnPay_export'),
    path('download/TraTIenSoi/<int:year>', views.export_YarnPay, name='YarnPay_export'),
    path('download/CongNoSoi/', views.export_YarnDebt, name='YarnDebt_export'),
    path('download/CongNoSoi/<int:year>', views.export_YarnDebt, name='YarnDebt_export'),
]
