from collections import deque
from datetime import datetime, timedelta, date
from decimal import Decimal

from django.core import serializers
from django.db import models

from django.db.models.functions import ExtractMonth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, Q, Avg, Min, Max
from sale_manage.models import Sales, Customer_Debt, Customer_Pay, Returned
from QLSanXuat.models import Det_Tay, KhoTay
from yarn_manage.models import Delivery, YarnDebt_LY, YarnPay, YarnTransfer, Warehouse, YarnVendor
from .models import spandex_default_rate
from django.http import JsonResponse
import random as random

def separate_list(input_list, chunk_size):
    return [input_list[i:i+chunk_size] for i in range(0, len(input_list), chunk_size)]

def month_list_func():
    today = date.today()
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    month_list = deque(month_list)
    month_list.rotate(-today.month)
    month_list = list(month_list)
    return month_list

def months_func():
    today =date.today()
    months = [today.strftime('%m / %Y')]
    for _ in range(11):
        today -= timedelta(days=30)
        months.insert(0, today.strftime('%m / %Y'))
    return months
# Create your views here.

@login_required
def main_page(request):
    return render(request, 'dashboard/main_page.html',)


@login_required
def dashboard_sale(request, year=datetime.now().year):
    sale_year = Sales.objects.filter(year=year)
    returned_year = Returned.objects.filter(year=year)
    month_list = month_list_func()
    months = months_func()
    # calculate spandex_weight
    if request.user.is_superuser:
        check = spandex_default_rate.objects.filter(id=1)
        if not check.exists():
            spandex_default_rate.objects.create(id=1, spandex_rate=request.GET.get('sd_def_rate'))
        else:
            obj = spandex_default_rate.objects.get(id=1)
            obj.save(sd=request.GET.get('sd_def_rate'))
    spandex_rate = spandex_default_rate.objects.get(id=1).spandex_rate
    spandex_rate_weight = Det_Tay.objects.filter(year=year, RE=False).values('Spandex_rate', 'Weight')
    for item in spandex_rate_weight:
        if item['Spandex_rate'] is None:
            item['Spandex_rate'] = spandex_rate
    total_spandex_weight = 0
    for item in spandex_rate_weight:
        total_spandex_weight += item['Spandex_rate'] * item['Weight']/100
    total_spandex_weight = round(total_spandex_weight, 2)
    # Ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Chart_1
        top_sales = sale_year.values('Customer__name').annotate(BuyValue=Sum('Amount')).order_by(
            '-BuyValue')[:5]
        other_sales = sale_year.exclude(
            Customer__name__in=[item['Customer__name'] for item in top_sales]).aggregate(BuyValue=Sum('Amount'))
        C1_labels_qs1 = [item['Customer__name'] for item in top_sales]
        C1_values_qs1 = [float(item['BuyValue']) or 0 for item in top_sales]
        if other_sales['BuyValue']:
            C1_labels_qs1.append('Khác')
            C1_values_qs1.append(float(other_sales['BuyValue']) or 0)

        # Chart_2
        top_debts = Customer_Debt.objects.filter(Year=year).values('Customer__name').annotate(
            DebtValue=Sum('Amount')).order_by(
            '-DebtValue')[:5]
        other_debts = Customer_Debt.objects.filter(Year=year).exclude(
            Customer__name__in=[item['Customer__name'] for item in top_debts]).aggregate(DebtValue=Sum('Amount'))
        C2_labels_qs1 = [item['Customer__name'] for item in top_debts]
        C2_values_qs1 = [float(item['DebtValue']) or 0 for item in top_debts]
        if other_debts['DebtValue']:
            C2_labels_qs1.append('Khác')
            C2_values_qs1.append(float(other_debts['DebtValue']) or 0)

        # Chart 3
        top_pay = Customer_Pay.objects.filter(year=year).values('Customer__name').annotate(
            PayValue=Sum('Amount')).order_by('-PayValue')[:5]
        other_pay = Customer_Pay.objects.filter(year=year).exclude(
            Customer__name__in=[item['Customer__name'] for item in top_pay]).aggregate(PayValue=Sum('Amount'))
        C3_labels_qs1 = [item['Customer__name'] for item in top_pay]
        C3_values_qs1 = [float(item['PayValue']) or 0 for item in top_pay]
        if other_pay['PayValue']:
            C3_labels_qs1.append('Khác')
            C3_values_qs1.append(float(other_pay['PayValue']) or 0)

        # returned_ratio
        total_sales = sale_year.aggregate(Tt_NetWeight=Sum('Net_Weight'), )
        total_return = returned_year.aggregate(Tt_NetWeight=Sum('Net_Weight'))
        try:
            returned_ratio = round(float(total_return['Tt_NetWeight']) / float(total_sales['Tt_NetWeight']) * 100, 2)
        except:
            returned_ratio = 0.00

        # total_debt
        total_sales = Sales.objects.filter(year=year).aggregate(Sum('Amount'))
        # total_debt
        total_debt = Customer_Debt.objects.filter(Year=year).aggregate(Sum('Amount'))
        # total_pay
        total_pay = Customer_Pay.objects.filter(year=year).aggregate(Sum('Amount'))
        # % returned
        returned_M = returned_year.filter(Final_Product='M').aggregate(Tt_NetWeight=Sum('Net_Weight'))
        returned_N = returned_year.filter(Final_Product='N').aggregate(Tt_NetWeight=Sum('Net_Weight'))
        returned_I = returned_year.filter(Final_Product='I').aggregate(Tt_NetWeight=Sum('Net_Weight'))

        M_pc = 0.00
        N_pc = 0.00
        I_pc = 0.00
        if returned_ratio > 0:
            try:
                M_pc = round(float(returned_M['Tt_NetWeight']) / float(total_return['Tt_NetWeight']) * 100, 2)
            except:
                pass
            try:
                N_pc = round(float(returned_N['Tt_NetWeight']) / float(total_return['Tt_NetWeight']) * 100, 2)
            except:
                pass
            try:
                I_pc = round(float(returned_I['Tt_NetWeight']) / float(total_return['Tt_NetWeight']) * 100, 2)
            except:
                pass
        # Chart 4
        today = date.today()
        start_date = today - timedelta(365)
        revenue_data = Sales.objects.filter(Date__range=[start_date, today]).annotate(month=ExtractMonth('Date')) \
            .values('month', 'year').annotate(revenue=Sum('Amount')).order_by('year', 'month')

        month_revenue_dict = {item['month']: item['revenue'] for item in revenue_data}
        for month in month_list:
            month_revenue_dict.setdefault(month, 0)
        revenue_data = [{'month': month, 'revenue': month_revenue_dict[month]} for month in month_list]

        C4_labels_qs1 = months
        C4_values_qs1 = [float(item['revenue']) for item in revenue_data]
        # Chart 5
        final_product_choices = {
            'M': 'Mộc',
            'N': 'Nhuộm',
            'I': 'In',
        }
        sales_by_final_product = sale_year.values('Final_Product').annotate(WeightValue=Sum('Weight')).order_by('-WeightValue')
        C5_labels_qs1 = [final_product_choices[item['Final_Product']] for item in sales_by_final_product]
        C5_values_qs1 = [float(item['WeightValue']) or 0 for item in sales_by_final_product]
        # sale weight
        Sale_weight = sale_year.aggregate(Tt_Weight=Sum('Weight'))
        Sale_Net_Weight = sale_year.aggregate(Tt_NetWeight=Sum('Net_Weight'))
        # Chart 6
        sales_by_product_type = sale_year.values('Product_Type').annotate(WeightValue=Sum('Weight')).order_by(
            '-WeightValue')[:5]
        other_sales_by_product_type = sale_year.exclude(
            Product_Type__in=[item['Product_Type'] for item in sales_by_product_type]).aggregate(
            WeightValue=Sum('Weight'))
        C6_labels_qs1 = [item['Product_Type'] for item in sales_by_product_type]
        C6_values_qs1 = [float(item['WeightValue']) or 0 for item in sales_by_product_type]
        if other_sales_by_product_type['WeightValue']:
            C6_labels_qs1.append('Khác')
            C6_values_qs1.append(float(other_sales_by_product_type['WeightValue']) or 0)

        updated_data = {
            'C1_labels_qs1': C1_labels_qs1, 'C1_values_qs1': C1_values_qs1, 'total_sales': total_sales,
            'C2_labels_qs1': C2_labels_qs1, 'C2_values_qs1': C2_values_qs1, 'total_debt': total_debt,
            'C3_labels_qs1': C3_labels_qs1, 'C3_values_qs1': C3_values_qs1, 'total_pay': total_pay,
            'returned_ratio': returned_ratio, 'limit': 2,
            'M_pc': M_pc, 'N_pc': N_pc, 'I_pc': I_pc,
            'C4_labels_qs1': C4_labels_qs1, 'C4_values_qs1': C4_values_qs1,
            'C5_labels_qs1': C5_labels_qs1, 'C5_values_qs1': C5_values_qs1, 'Sale_Weight': Sale_weight, 'Sale_NetWeight': Sale_Net_Weight,
            'C6_labels_qs1': C6_labels_qs1, 'C6_values_qs1': C6_values_qs1,
        }

        return JsonResponse(updated_data)
    else:
        # Handle regular HTML request
        context = {
            'title': 'Sale Analysis',
            'year': year,
            'C1_name': f'Khách Mua Hàng {year} (Top 5)',
            'C2_name': f'Công Nợ Khách Hàng {year} (Top 5)',
            'C3_name': f'Khách Hàng Trả Tiền {year} (Top 5)',
            'C4_name': 'Bán Hàng Trong 12 Tháng Gần Nhất',
            'C5_name': f'Bán Hàng Theo Thành Phẩm {year} (KL:kg)',
            'C6_name': f'Bán Hàng Theo Phân Loại Hàng {year} (KL:kg)',
            'spandex_rate': spandex_rate, 'total_spandex_weight': total_spandex_weight,
        }

        return render(request, 'dashboard/dashboard_sale.html', context)

@login_required
def dashboard_production(request, year=datetime.now().year):
    month_list = month_list_func()
    months = months_func()
    # calculate spandex_weight
    if request.user.is_superuser:
        check = spandex_default_rate.objects.filter(id=1)
        if not check.exists():
            spandex_default_rate.objects.create(id=1, spandex_rate=request.GET.get('sd_def_rate'))
        else:
            obj = spandex_default_rate.objects.get(id=1)
            obj.save(sd=request.GET.get('sd_def_rate'))
    spandex_rate = spandex_default_rate.objects.get(id=1).spandex_rate
    spandex_rate_weight = Det_Tay.objects.filter(year=year, RE=False).values('Spandex_rate', 'Weight')
    for item in spandex_rate_weight:
        if item['Spandex_rate'] is None:
            item['Spandex_rate'] = spandex_rate
    total_spandex_weight = 0
    for item in spandex_rate_weight:
        total_spandex_weight += item['Spandex_rate'] * item['Weight'] / 100
    total_spandex_weight = round(total_spandex_weight, 2)
    # Ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Chart 11
        today = date.today()
        start_date = today - timedelta(365)
        Weaving_yield = Det_Tay.objects.filter(Date__range=[start_date, today], FromWhere__isnull=False).annotate(
            month=ExtractMonth('Date')) \
            .values('month').annotate(Tt_Weight=Sum('Weight')).order_by('year', 'month')
        month_TtWeight_dict = {item['month']: item['Tt_Weight'] for item in Weaving_yield}
        for month in month_list:
            month_TtWeight_dict.setdefault(month, 0)
        Weaving_yield = [{'month': month, 'Tt_Weight': month_TtWeight_dict[month]} for month in month_list]
        C11_labels_qs1 = months
        C11_values_qs1 = [float(item['Tt_Weight']) for item in Weaving_yield]
        # Chart 12
        yield_by_FromWhere = Det_Tay.objects.filter(year=year, RE=False).values('FromWhere__KhoDet') \
            .annotate(Tt_Weight=Sum('Weight')).order_by('-Tt_Weight')[:3]
        yield_by_others = Det_Tay.objects.filter(year=year, RE=False).exclude(
            FromWhere__KhoDet__in=[item['FromWhere__KhoDet'] for item in yield_by_FromWhere]).aggregate(
            Tt_Weight=Sum('Weight'))
        C12_labels_qs1 = [item['FromWhere__KhoDet'] for item in yield_by_FromWhere]
        C12_values_qs1 = [float(item['Tt_Weight']) or 0 for item in yield_by_FromWhere]
        if yield_by_others['Tt_Weight']:
            C12_labels_qs1.append('Khác')
            C12_values_qs1.append(float(yield_by_others['Tt_Weight']) or 0)
        # total weaving yield
        Total_weaving_yield = Det_Tay.objects.filter(year=year, RE=False).aggregate(Sum('Weight'))
        # Chart 13
        yield_by_pc = Det_Tay.objects.filter(year=year, RE=False).values('Product_class__Product_class') \
                          .annotate(Tt_Weight=Sum('Weight')).order_by('-Tt_Weight')[:5]
        yield_by_other_pc = Det_Tay.objects.filter(year=year, RE=False).exclude(
            Product_class__Product_class__in=[item['Product_class__Product_class'] for item in yield_by_pc]).aggregate(
            Tt_Weight=Sum('Weight'))
        C13_labels_qs1 = [item['Product_class__Product_class'] for item in yield_by_pc]
        C13_values_qs1 = [float(item['Tt_Weight']) or 0 for item in yield_by_pc]
        if yield_by_other_pc['Tt_Weight']:
            C13_labels_qs1.append('Khác')
            C13_values_qs1.append(float(yield_by_other_pc['Tt_Weight']) or 0)
        # count number of default spandex
        null_count = Det_Tay.objects.filter(year=year, Spandex_rate__isnull=True).count()
        all_count = Det_Tay.objects.filter(year=year).count()
        # Char 14,15,16
        Positive_CS = Det_Tay.objects.filter(CS__gt=0)
        # Chart 14
        CS_by_Product_class = Positive_CS.values('Product_class__Product_class') \
                                  .annotate(Tt_CS=Sum('CS')).order_by('-Tt_CS')[:5]
        C14_labels_qs1 = [item['Product_class__Product_class'] for item in CS_by_Product_class]
        C14_values_qs1 = [float(item['Tt_CS']) or 0 for item in CS_by_Product_class]
        other_CS_by_Product_class = Positive_CS.exclude(
            Product_class__Product_class__in=[item['Product_class__Product_class'] for item in
                                              CS_by_Product_class]).aggregate(Tt_CS=Sum('CS'))
        if other_CS_by_Product_class['Tt_CS']:
            C14_labels_qs1.append('Khác')
            C14_values_qs1.append(other_CS_by_Product_class['Tt_CS'])
        # Chart 15
        CS_by_Location = Positive_CS.values('Destination__KhoTay') \
                             .annotate(Tt_CS=Sum('CS')).order_by('-Tt_CS')[:5]
        C15_labels_qs1 = [item['Destination__KhoTay'] for item in CS_by_Location]
        C15_values_qs1 = [float(item['Tt_CS']) or 0 for item in CS_by_Location]
        other_CS_by_Location = Positive_CS.exclude(
            Destination__KhoTay__in=[item['Destination__KhoTay'] for item in
                                     CS_by_Location]).aggregate(Tt_CS=Sum('CS'))
        if other_CS_by_Location['Tt_CS']:
            C15_labels_qs1.append('Khác')
            C15_values_qs1.append(other_CS_by_Location['Tt_CS'])
        # Chart 16
        CS_by_year = Positive_CS.values('year').annotate(Tt_CS=Sum('CS')).order_by('-year')[:3]
        C16_labels_qs1 = [item['year'] for item in CS_by_year]
        C16_values_qs1 = [float(item['Tt_CS']) or 0 for item in CS_by_year]
        other_CS_by_year = Positive_CS.exclude(
            year__in=[item['year'] for item in
                      CS_by_year]).aggregate(Tt_CS=Sum('CS'))
        if other_CS_by_year['Tt_CS']:
            C16_labels_qs1.append('Khác')
            C16_values_qs1.append(other_CS_by_year['Tt_CS'])
        updated_data = {
            'C11_labels_qs1': C11_labels_qs1, 'C11_values_qs1': C11_values_qs1,
            'C12_labels_qs1': C12_labels_qs1, 'C12_values_qs1': C12_values_qs1,
            'Total_weaving_yield': Total_weaving_yield,
            'C13_labels_qs1': C13_labels_qs1, 'C13_values_qs1': C13_values_qs1,
            'total_spandex_weight': total_spandex_weight, 'spandex_rate': spandex_rate, 'null_count': null_count,
            'all_count': all_count,
            'C14_labels_qs1': C14_labels_qs1, 'C14_values_qs1': C14_values_qs1,
            'C15_labels_qs1': C15_labels_qs1, 'C15_values_qs1': C15_values_qs1,
            'C16_labels_qs1': C16_labels_qs1, 'C16_values_qs1': C16_values_qs1,
        }

        return JsonResponse(updated_data)
    else:
        # Handle regular HTML request
        options = KhoTay.objects.values_list('KhoTay', flat=True)
        warehouse_name = request.GET.get('warehouse-selection')
        stock_results = Det_Tay.objects.filter(CS__gt=0, Destination__KhoTay=warehouse_name).values('Product_class__Product_class') \
            .annotate(Tt_CS=Sum('CS'), Tt_CS_PreviousYears=Sum(Case(When(Q(year__lt=year), then='CS'), default=0,
                                                                    output_field=models.IntegerField()))).order_by('-Tt_CS')

        context = {
            'title': 'Production Analysis',
            'year': year,
            'C11_name': 'Sản Lượng Dệt 12 Tháng Gần Nhất',
            'C12_name': f'Sản Lượng Các Xưởng Dệt 2023 (Top 3)',
            'C13_name': f'Sản Lượng Theo Phân Loại Hàng {year} (KL:kg)',
            'C14_name': 'Tồn Kho Mộc Theo Phân Loại Hàng (Số Cây)',
            'C15_name': 'Tồn Kho Mộc Tại Các Lò Tẩy (Số Cây)',
            'C16_name': 'Tồn Kho Mộc Theo Năm Xuất Đi (Số Cây)',
            'spandex_rate': spandex_rate, 'total_spandex_weight': total_spandex_weight,
            'options': options, 'WH_name': warehouse_name, 'stock_results': stock_results,
        }
    return render(request, 'dashboard/dashboard_production.html', context)


@login_required
def dashboard_procure(request, year=datetime.now().year):
    month_list = month_list_func()
    months = months_func()
    Delivery_year = Delivery.objects.filter(year=year)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Chart 21
        Delivery_by_supplier = Delivery_year.values('OrderID__Vendor__Name') \
                               .annotate(Tt_Weight=Sum('Weight')).order_by('-Tt_Weight')[:5]
        Other_Delivery_by_supplier = Delivery_year.exclude(
            OrderID__Vendor__Name__in=[item['OrderID__Vendor__Name'] for item in Delivery_by_supplier]).aggregate(
            Tt_Weight=Sum('Weight'))
        C21_labels_qs1 = [item['OrderID__Vendor__Name'] for item in Delivery_by_supplier]
        C21_values_qs1 = [float(item['Tt_Weight']) for item in Delivery_by_supplier]
        if Other_Delivery_by_supplier['Tt_Weight']:
            C21_labels_qs1.append('Khác')
            C21_values_qs1.append(float(Other_Delivery_by_supplier['Tt_Weight']))
        # Chart 22
        Delivery_by_class = Delivery_year.values('OrderID__YarnType__Name').annotate(Tt_Weight=Sum('Weight')).order_by('-Tt_Weight')[:5]
        Other_Delivery_by_class = Delivery_year.exclude(
            OrderID__YarnType__Name__in=[item['OrderID__YarnType__Name'] for item in Delivery_by_class]).aggregate(
            Tt_Weight=Sum('Weight'))
        C22_labels_qs1 = [item['OrderID__YarnType__Name'] for item in Delivery_by_class]
        C22_values_qs1 = [float(item['Tt_Weight']) for item in Delivery_by_class]
        if Other_Delivery_by_class['Tt_Weight']:
            C22_labels_qs1.append('Khác')
            C22_values_qs1.append(float(Other_Delivery_by_class['Tt_Weight']))

        # Chart 23
        YarnDebt = YarnDebt_LY.objects.filter(Year=year).values('Vendor__Name').annotate(
            Tt_Debt=Sum('Debt')).order_by('-Tt_Debt')[:5]
        Other_YarnDebt = YarnDebt_LY.objects.filter(Year=year).exclude(
            Vendor__Name__in=[item['Vendor__Name'] for item in YarnDebt]).aggregate(Tt_Debt=Sum('Debt'))
        C23_labels_qs1 = [item['Vendor__Name'] for item in YarnDebt]
        C23_values_qs1 = [float(item['Tt_Debt']) for item in YarnDebt]
        if Other_YarnDebt['Tt_Debt']:
            C23_labels_qs1.append('Khác')
            C23_values_qs1.append(float(Other_YarnDebt['Tt_Debt']))
        # Total Delivery Amount
        Tt_Delivery_Amount = Delivery.objects.filter(year=year).aggregate(Sum('PayValue'))
        # Total Debt
        Tt_Debt = YarnDebt_LY.objects.filter(Year=year).aggregate(Sum('Debt'))
        Tt_Debt_LY = YarnDebt_LY.objects.filter(Year=year).aggregate(Sum('Debt_LY'))
        # Total Pay
        Tt_Pay = YarnPay.objects.filter(year=year).aggregate(Sum('Pay'))
        # Chart 24
        Tt_Yarn_In = YarnTransfer.objects.filter(year=year, Destination__WH_Type='D').values('Destination__Name') \
            .annotate(Tt_In=Sum('Weight')).order_by('-Tt_In')
        Tt_Yarn_Out = YarnTransfer.objects.filter(year=year, Origin__Name__WH_Type='D', Origin__isnull=False) \
            .values('Origin__Name__Name').annotate(Tt_Out=Sum('Weight'))
        for item in Tt_Yarn_In:
            for item2 in Tt_Yarn_Out:
                if item['Destination__Name'] == item2['Origin__Name__Name']:
                    item['Tt_In'] = item['Tt_In'] - item2['Tt_Out']
        Tt_Yarn_InOut = Tt_Yarn_In[:3]
        Other_Yarn_InOut = Tt_Yarn_In[3:]
        Other_Yarn_sum = 0
        for item in Other_Yarn_InOut:
            Other_Yarn_sum += item['Tt_In']
        C24_labels_qs1 = [item['Destination__Name'] for item in Tt_Yarn_InOut]
        C24_values_qs1 = [float(item['Tt_In']) for item in Tt_Yarn_InOut]
        C24_values_qs2 = []
        Tt_Production = Det_Tay.objects.filter(year=year, RE=False).values('FromWhere__KhoDet').annotate(Tt_Weight=Sum('Weight'))
        other_value = 0
        for item in C24_labels_qs1:
            value = 0
            for item2 in Tt_Production:
                if item == item2['FromWhere__KhoDet'] and value == 0:
                    value = float(item2['Tt_Weight'])
                elif item != item2['FromWhere__KhoDet']:
                    other_value += item2['Tt_Weight']
            C24_values_qs2.append(value)
        if Other_Yarn_sum > 0:
            C24_labels_qs1.append('Khác')
            C24_values_qs1.append(float(Other_Yarn_sum))
            C24_values_qs2.append(float(other_value))
        # Chart 25
        today = date.today()
        start_date = today - timedelta(365)
        yarn_pay_data = YarnPay.objects.filter(Date__range=[start_date, today]).annotate(month=ExtractMonth('Date')) \
            .values('month', 'year').annotate(Tt_Pay=Sum('Pay')).order_by('year', 'month')

        month_yarn_pay_dict = {item['month']: item['Tt_Pay'] for item in yarn_pay_data}
        for month in month_list:
            month_yarn_pay_dict.setdefault(month, 0)
        yarn_pay_data = [{'month': month, 'Tt_Pay': month_yarn_pay_dict[month]} for month in month_list]

        C25_labels_qs1 = months
        C25_values_qs1 = [float(item['Tt_Pay']) for item in yarn_pay_data]

        updated_data = {
            'C21_labels_qs1': C21_labels_qs1, 'C21_values_qs1': C21_values_qs1,
            'C22_labels_qs1': C22_labels_qs1, 'C22_values_qs1': C22_values_qs1,
            'C23_labels_qs1': C23_labels_qs1, 'C23_values_qs1': C23_values_qs1,
            'C24_labels_qs1': C24_labels_qs1, 'C24_values_qs1': C24_values_qs1, 'C24_values_qs2': C24_values_qs2,
            'C25_labels_qs1': C25_labels_qs1, 'C25_values_qs1': C25_values_qs1,
            'Tt_Delivery_Amount': Tt_Delivery_Amount, 'Tt_Debt': Tt_Debt, 'Tt_Debt_LY': Tt_Debt_LY, 'Tt_Pay': Tt_Pay
        }
        return JsonResponse(updated_data)
    else:
        # Price
        VD_options = YarnVendor.objects.values_list('Name', flat=True).order_by('id')
        vendor_name = request.GET.get('VD-selection')
        if vendor_name == 'Tất Cả':
            Delivery_Price = Delivery.objects.filter(year=year).values('OrderID__YarnType__Name') \
                .annotate(avg_price=Avg('Price'), min_price=Min('Price'), max_price=Max('Price'))
        else:
            Delivery_Price = Delivery.objects.filter(year=year, OrderID__Vendor__Name=vendor_name).values('OrderID__YarnType__Name') \
                .annotate(avg_price=Avg('Price'), min_price=Min('Price'), max_price=Max('Price'))
        for item in Delivery_Price:
            item['avg_price'] = round(item['avg_price'], 2)

        # XN Sợi
        WH_options = Warehouse.objects.values_list('Name', flat=True).order_by('id')
        warehouse_name = request.GET.get('WH-selection')
        YarnTransfer_year = YarnTransfer.objects.filter(year=year)
        Yarn_In_Out = YarnTransfer_year.values('YarnType__Name') \
            .annotate(Tt_Weight_In=Sum(Case(When(Q(Destination__Name=warehouse_name), then='Weight'), default=0,
            output_field=models.DecimalField())), Tt_Weight_Out=Sum(Case(When(Q(Origin__Name__Name=warehouse_name), then='Weight'), default=0,
            output_field=models.DecimalField())))
        Yarn_In_Out = [item for item in Yarn_In_Out if item['Tt_Weight_In'] != 0 or item['Tt_Weight_Out'] != 0]
        for item in Yarn_In_Out:
            item['WIO'] = item['Tt_Weight_In'] - item['Tt_Weight_Out']

        context = {
            'title': 'Procurement Analysis',
            'year': year,
            'C21_name': f'Sợi Đã Giao Theo NBH {year}',
            'C22_name': f'Sợi Đã Giao Theo Phân Loại {year}',
            'C23_name': f'Công Nợ Sợi {year}',
            'C24_name': f'Nhập Sợi và Sản Xuất {year}',
            'C25_name': 'Trả Tiền Sợi 12 Tháng Gần Nhất',
            'VD_options': VD_options, 'VD_name': vendor_name, 'Delivery_Price': Delivery_Price,
            'WH_options': WH_options, 'WH_name': warehouse_name, 'Yarn_In_Out': Yarn_In_Out,
        }
        return render(request, 'dashboard/dashboard_procure.html', context)