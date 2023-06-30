from django.urls import path
from . import views

urlpatterns = [
    path('sales_hn/<int:year>/', views.sales_hn, name='sales_hn'),
    path('sales/<int:year>/', views.sales, name='sales'),
    path('sales/add/', views.sales_add, name='sales_add'),
    path('sales/delete/<int:pk>/', views.sales_delete, name='sales_delete'),
    path('sales/update/<int:pk>/', views.sales_update, name='sales_update'),

    path('returned_hn/<int:year>/', views.returned_hn, name='returned_hn'),
    path('return/<int:year>/', views.returned, name='returned'),
    path('returned/add/', views.returned_add, name='returned_add'),
    path('returned/delete/<int:pk>', views.returned_delete, name='returned_delete'),
    path('returned/update/<int:pk>', views.returned_update, name='returned_update'),

    path('customer_pay_hn/<int:year>/', views.Pay_hn, name='Pay_hn'),
    path('customer_pay/<int:year>/', views.Pay, name='Pay'),
    path('customer_pay/add/', views.Pay_add, name='Pay_add'),
    path('customer_pay/delete/<int:pk>', views.Pay_delete, name='Pay_delete'),
    path('customer_pay/update/<int:pk>', views.Pay_update, name='Pay_update'),

    path('customer_debt/<int:year>/', views.Debt, name='Customer_Debt'),
    path('customer_debt/add/<int:Customer_id>/<int:Year>', views.Customer_Debt_add, name='Customer_Debt_add'),
    path('customer_debt/update/<int:Customer_id>/<int:Year>', views.Customer_Debt_update, name='Customer_Debt_update'),

    path('download/Sales/', views.export_Sales, name='Sales_export'),
    path('download/Sales/<int:year>', views.export_Sales, name='Sales_export'),
    path('download/Returned/', views.export_Returned, name='Returned_export'),
    path('download/Returned/<int:year>', views.export_Returned, name='Returned_export'),
    path('download/CtmPay/', views.export_CtmPay, name='CtmPay_export'),
    path('download/CtmPay/<int:year>', views.export_CtmPay, name='CtmPay_export'),
    path('download/CtmDebt/', views.export_CtmDebt, name='CtmDebt_export'),
    path('download/CtmDebt/<int:year>', views.export_CtmDebt, name='CtmDebt_export'),
]