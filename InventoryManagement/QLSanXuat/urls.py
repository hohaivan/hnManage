from django.urls import path
from . import views

urlpatterns = [
    path('weave-bleach-hn/<int:year>', views.WeaveBleach_hn, name='Det_Tay_hn'),
    path('weave-bleach/<int:year>/', views.WeaveBleach, name='Det_Tay'),
    path('weave-bleach/add/', views.WeaveBleach_add, name='Det_Tay_add'),
    path('weave-bleach/delete/<int:pk>/', views.WeaveBleach_delete, name='Det_Tay_delete'),
    path('weave-bleach/update/<int:pk>/', views.WeaveBleach_update, name='Det_Tay_update'),
    path('weave-bleach/view/<int:pk>/', views.WeaveBleach_detail, name='Det_Tay_detail'),

    path('bleach-raw-hn/<int:year>/', views.BleachRaw_hn, name='Tay_Moc_hn'),
    path('bleach-raw/<int:year>/', views.BleachRaw, name='Tay_Moc'),
    path('bleach-raw/add/<int:pk>/', views.BleachRaw_add, name='Tay_Moc_add'),
    path('bleach-raw/delete/<int:pk>/', views.BleachRaw_delete, name='Tay_Moc_delete'),
    path('bleach-raw/update/<int:pk>/', views.BleachRaw_update, name='Tay_Moc_update'),

    path('bleach-print-hn/<int:year>', views.BleachPrint_hn, name='Tay_In_hn'),
    path('bleach-print/<int:year>', views.BleachPrint, name='Tay_In'),
    path('bleach-print/add/<int:pk>', views.BleachPrint_add, name='Tay_In_add'),
    path('bleach-print/delete/<int:pk>', views.BleachPrint_delete, name='Tay_In_delete'),
    path('bleach-print/update/<int:pk>', views.BleachPrint_update, name='Tay_In_update'),

    path('bleach-dye-hn/<int:year>', views.BleachDye_hn, name='Tay_Nhuom_hn'),
    path('bleach-dye/<int:year>', views.BleachDye, name='Tay_Nhuom'),
    path('bleach-dye/add/<int:pk>', views.BleachDye_add, name='Tay_Nhuom_add'),
    path('bleach-dye/delete/<int:pk>', views.BleachDye_delete, name='Tay_Nhuom_delete'),
    path('bleach-dye/update/<int:pk>', views.BleachDye_update, name='Tay_Nhuom_update'),

    path('stretch-hn/<int:year>/', views.Stretch_hn, name='Cang_hn'),
    path('stretch/<int:year>/', views.Stretch, name='Cang'),
    path('print-stretch/add/<int:pk>/', views.In_Cang, name='In_Cang_add'),
    path('dye-stretch/add/<int:pk>/', views.Nhuom_Cang, name='Nhuom_Cang_add'),
    path('stretch/delete/<int:pk>', views.Stretch_delete, name='Cang_delete'),
    path('stretch/update/<str:batch>', views.Stretch_update, name='Cang_update'),

    path('download/Det_Tay/', views.export_Det_Tay, name='Det_Tay_export'),
    path('download/Det_Tay/<int:year>', views.export_Det_Tay, name='Det_Tay_export'),
    path('download/Tay_Moc/', views.export_Tay_Moc, name='Tay_Moc_export'),
    path('download/Tay_Moc/<int:year>', views.export_Tay_Moc, name='Tay_Moc_export'),
    path('download/Tay_In/', views.export_Tay_In, name='Tay_In_export'),
    path('download/Tay_In/<int:year>', views.export_Tay_In, name='Tay_In_export'),
    path('download/Tay_Nhuom', views.export_Tay_Nhuom, name='Tay_Nhuom_export'),
    path('download/Tay_Nhuom/<int:year>', views.export_Tay_Nhuom, name='Tay_Nhuom_export'),
    path('download/Cang/', views.export_Cang, name='Cang_export'),
    path('download/Cang/<int:year>', views.export_Cang, name='Cang_export'),
]
