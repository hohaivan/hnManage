from datetime import datetime, date
from decimal import Decimal

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, DecimalField, Subquery, OuterRef, Max
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from QLSanXuat.models import KhachHang
from .models import Sales, Returned, Customer_Debt, Customer_Pay
from .forms import sales_form, returned_form, customer_pay_form, customer_debt_form
from supports.export_excel import export_by_year, get_model_by_name, export_to_excel
import supports.generate_filter as gf


@login_required
def export_Sales(request, app='sale_manage', model='Sales', name='Ban_Hang'):
    return export_by_year(request, app, model, name)

@login_required
def export_Returned(request, app='sale_manage', model='Returned', name='Hang_Tra'):
    return export_by_year(request, app, model, name)

@login_required
def export_CtmPay(request, app='sale_manage', model='Customer_Pay', name='KH_Tra_Tien'):
    return export_by_year(request, app, model, name)

@login_required
def export_CtmDebt(request):
    app_label = 'sale_manage'
    model_name = 'Customer_Debt'
    year = request.GET.get('year')
    Model = get_model_by_name(app_label, model_name)
    if Model is not None:
        filter_params = {'Year': year}
        order_by = ['Customer']
        filename = f'Cong_No_KH_{year}_at_{datetime.today().date()}.xlsx'
        return export_to_excel(request, Model, filter_params, order_by, filename)
    else:
        raise ValueError("Model not found.")


@login_required
def sales_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'PXK', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': None,
        },
        {
            'field_name': 'Customer', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': 'name',
        },
        {
            'field_name': 'Product_Name', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
        {
            'field_name': 'Product_Type', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': None,
        },
        {
            'field_name': 'Final_Product', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': None,
        },
        {
            'field_name': 'Colours', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Patterns', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Qty', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
        {
            'field_name': 'Cut', 'filter_input': request.GET.get('col11_filter'),
            'filter_option': request.GET.get('filter_option_11'), 'related_name': None,
        },
        {
            'field_name': 'Net_Weight', 'filter_input': request.GET.get('col12_filter'),
            'filter_option': request.GET.get('filter_option_12'), 'related_name': None,
        },
        {
            'field_name': 'Price', 'filter_input': request.GET.get('col13_filter'),
            'filter_option': request.GET.get('filter_option_13'), 'related_name': None,
        },
        {
            'field_name': 'Amount', 'filter_input': request.GET.get('col14_filter'),
            'filter_option': request.GET.get('filter_option_14'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Sales.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Sales.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'number'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'),
                           ('7', 'text'), ('8', 'text'), ('9', 'number'), ('10', 'number'), ('11', 'number'),
                           ('12', 'number'), ('13', 'number'), ('14', 'number'),
                           ]
    context = {
        'nav': 'sales',
        'year': year,
        'hn': hn,
        'rows': rows,
        'selection_generator': selection_generator,
        'types': Sales.FP_Choices,
    }
    return render(request, 'sales_manage/sales/sales.html', context)


@login_required
def sales(request, year=datetime.now().year):
    return sales_hn(request, year=year, hn=False)


@login_required
def sales_add(request):
    if request.method == 'POST':
        form = sales_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            # generate success message and redirect after saving
            success_message = f'Đã Thêm Thành Công Đơn Hàng Cho PXK: {instance.PXK}<br>Khách Hàng: {instance.Customer}'
            messages.success(request, mark_safe(success_message))
            return redirect(reverse('sales_add'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = sales_form(initial={'Date': datetime.now().date()})

    context = {
        'nav': 'sales',
        'form': form,
    }
    return render(request, 'sales_manage/sales/sales_add.html', context)


@login_required
def sales_delete(request, pk):
    row = Sales.objects.get(id=pk)
    if request.method == 'POST':
        if request.user.is_superuser or request.user == row.Creator:
            row.delete()
            return redirect(reverse('sales_hn', args=[row.year]))
        else:
            messages.error(request, 'Permission Blocked')
            return redirect(reverse('user-logout'))
    context = {
        'nav': 'sales',
        'row': row,
    }
    return render(request, 'sales_manage/sales/sales_delete.html', context)


@login_required
def sales_update(request, pk):
    row = Sales.objects.get(id=pk)
    if request. method == 'POST':
        if request.user.is_superuser or request.user == row.Creator:
            form = sales_form(request.POST, instance=row)
            if form.is_valid():
                form.save()
                return redirect(reverse('sales_hn', args=[row.year]))
            else:
                messages(request, f'Chưa Lưu Được')
        else:
            messages.error(request, 'Permission Blocked')
            return redirect(reverse('user-logout'))
    else:
        form = sales_form(instance=row)

    context = {
        'nav': 'sales',
        'form': form,
    }
    return render(request, 'sales_manage/sales/sales_update.html', context)


@login_required
def returned_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'Customer', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': 'name',
        },
        {
            'field_name': 'Product_Name', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
        {
            'field_name': 'Product_Type', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': None,
        },
        {
            'field_name': 'Final_Product', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': None,
        },
        {
            'field_name': 'Colours', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Patterns', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Qty', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
        {
            'field_name': 'Cut', 'filter_input': request.GET.get('col11_filter'),
            'filter_option': request.GET.get('filter_option_11'), 'related_name': None,
        },
        {
            'field_name': 'Net_Weight', 'filter_input': request.GET.get('col12_filter'),
            'filter_option': request.GET.get('filter_option_12'), 'related_name': None,
        },
        {
            'field_name': 'Price', 'filter_input': request.GET.get('col13_filter'),
            'filter_option': request.GET.get('filter_option_13'), 'related_name': None,
        },
        {
            'field_name': 'Amount', 'filter_input': request.GET.get('col14_filter'),
            'filter_option': request.GET.get('filter_option_14'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Returned.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Returned.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'),
                           ('7', 'text'), ('8', 'text'), ('9', 'number'), ('10', 'number'), ('11', 'number'),
                           ('12', 'number'), ('13', 'number'), ('14', 'number'),
                           ]
    context = {
        'nav': 'returned',
        'year': year,
        'hn': hn,
        'rows': rows,
        'selection_generator': selection_generator,
        'types': Returned.FP_Choices,
    }
    return render(request, 'sales_manage/return/returned.html', context)


@login_required
def returned(request, year=datetime.now().year):
    return returned_hn(request, year=year, hn=False)


@login_required
def returned_add(request):
    if request.method == 'POST':
        form = returned_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            # generate success message and redirect after saving
            success_message = f'Đã Thêm Thành Công Đơn Hàng Trả Của Khách Hàng: {instance.Customer}<br> Ngày: {instance.Date}'
            messages.success(request, mark_safe(success_message))
            return redirect(reverse('returned_add'))
        else:
            messages.error(request, f'Chưa Lưu Được')
    else:
        form = returned_form(initial={'Date': datetime.now().date()})

    context = {
        'nav': 'returned',
        'form': form,
    }
    return render(request, 'sales_manage/return/returned_add.html', context)


@login_required
def returned_delete(request, pk):
    row = Returned.objects.get(id=pk)
    if request.method == 'POST':
        if request.user.is_superuser or request.user == row.Creator:
            row.delete()
            return redirect(reverse('returned_hn', args=[row.year]))
        else:
            messages.error(request, 'Permission Blocked')
            return redirect(reverse('user-logout'))

    context = {
        'nav': 'returned',
        'row': row,

    }
    return render(request, 'sales_manage/return/returned_delete.html', context)


@login_required
def returned_update(request, pk):
    row = Returned.objects.get(id=pk)
    if request.method == 'POST':
        if request.user.is_superuser or request.user == row.Creator:
            form = returned_form(request.POST, instance=row)
            if form.is_valid():
                form.save()
                return redirect(reverse('returned_hn', args=[row.year]))
            else:
                messages(request, f'Chưa Lưu Được')
        else:
            messages.error(request, 'Permission Blocked')
            return redirect(reverse('user-logout'))
    else:
        form = returned_form(instance=row)

    context = {
        'nav': 'returned',
        'form': form,
    }
    return render(request, 'sales_manage/return/returned_update.html', context)


@login_required
def Pay_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'Customer', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'name',
        },
        {
            'field_name': 'Amount', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': None,
        },
        {
            'field_name': 'Sync', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Customer_Pay.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Customer_Pay.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'number'), ('4', 'text'), ]
    context = {
        'nav': 'Customer_Pay',
        'rows': rows,
        'year': year,
        'hn': hn,
        'selection_generator': selection_generator,
    }
    return render(request, 'sales_manage/pay/Customer_Pay.html', context)


@login_required
def Pay(request, year=datetime.now().year):
    return Pay_hn(request, year=year, hn=False)


@login_required
def Pay_add(request):
    if request.method == 'POST':
        form = customer_pay_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            # generate success message and redirect after saving
            success_message = f'Thêm Mới Thành Công:<br> Ngày: {instance.Date}, Khách Hàng: {instance.Customer} <br> Đã Trả Số Tiền: {instance.Amount}'
            messages.success(request, mark_safe(success_message))
            return redirect(reverse(Pay_add))
    else:
        form = customer_pay_form(initial={'Date':datetime.now().date()})
    context = {
        'nav': 'Customer_Pay',
        'form': form,
    }
    return render(request, 'sales_manage/pay/Customer_Pay_add.html', context)


@login_required
def Pay_delete(request, pk):
    row = Customer_Pay.objects.get(id=pk)
    if request.method == 'POST':
        if request.user.is_superuser or request.user == row.Creator:
            row.delete()
            return redirect(reverse('Pay_hn', args=[row.year]))
        else:
            messages.error(request, 'Permission Blocked')
            return redirect(reverse('user-logout'))
    context = {
        'nav': 'Customer_Pay',
        'row': row,
    }
    return render(request, 'sales_manage/pay/Customer_Pay_delete.html', context)


@login_required
def Pay_update(request, pk):
    row = Customer_Pay.objects.get(id=pk)
    if request.method == 'POST':
        if request.user.is_superuser or request.user == row.Creator:
            form = customer_pay_form(request.POST, instance=row)
            if form.is_valid():
                form.save()
                return redirect(reverse('Pay_hn', args=[row.year]))
            else:
                messages(request, f'Chưa Lưu Được')
        else:
            messages.error(request, 'Permission Blocked')
            return redirect(reverse('user-logout'))
    else:
        form = customer_pay_form(instance=row)

    context = {
        'nav': 'returned',
        'form': form,
    }
    return render(request, 'sales_manage/pay/Customer_Pay_update.html', context)


@login_required
def Debt(request, year=datetime.now().year):
    filter_date = request.GET.get('filter_date', date.today())
    rows = KhachHang.objects.all().order_by('id')
    debt_LY = Customer_Debt.objects.filter(Year=year - 1)
    Total_BuyValue = Sales.objects.filter(year=year, Date__lte=filter_date).values(
        'Customer__name').annotate(BuyValue=Sum('Amount'), Last_Sale=Max('Date'))

    Total_BackValue = Returned.objects.filter(year=year, Date__lte=filter_date).values(
        'Customer__name').annotate(BackValue=Sum('Amount'), Last_Back=Max('Date'))

    Total_PaidValue = Customer_Pay.objects.filter(year=year, Date__lte=filter_date).values(
        'Customer__name').annotate(PaidValue=Sum('Amount'), Last_Paid=Max('Date'))

    # Join the two querysets using a subquery expression
    Vendor_Queryset = KhachHang.objects.annotate(
        amount_old_debt=Coalesce(Subquery(
            debt_LY.filter(Customer=OuterRef('pk')).values('Amount')[:1],
            output_field=DecimalField()
        ), Decimal(0)),
        amount_bought_in=Coalesce(Subquery(
            Total_BuyValue.filter(Customer=OuterRef('pk')).values('BuyValue')[:1],
            output_field=DecimalField()
        ), Decimal(0)),
        amount_returned_back=Coalesce(Subquery(
            Total_BackValue.filter(Customer=OuterRef('pk')).values('BackValue')[:1],
            output_field=DecimalField()
        ), Decimal(0)),
        amount_paid=Coalesce(Subquery(
            Total_PaidValue.filter(Customer=OuterRef('pk')).values('PaidValue')[:1],
            output_field=DecimalField()
        ), Decimal(0)),
    )

    # Then you can annotate the vendor queryset with the debt value
    Debt_Queryset = Vendor_Queryset.annotate(
        debt_value=F('amount_old_debt', ) + F('amount_bought_in') - F('amount_returned_back') - F('amount_paid'))

    # Aggregates
    Grant_Old_Debt = debt_LY.aggregate(Sum('Amount'))
    Grant_BuyValue = Total_BuyValue.aggregate(Sum('BuyValue'))
    Grant_BackValue = Total_BackValue.aggregate(Sum('BackValue'))
    Grant_PaidValue = Total_PaidValue.aggregate(Sum('PaidValue'))
    Grant_DebtValue = Debt_Queryset.aggregate(Sum('debt_value'))
    context = {
        'nav': 'Customer_Debt',
        'filter_date': filter_date,
        'year': year,
        'last_year': year - 1,
        'rows': rows,
        'today': date.today(),
        'debt_LY': debt_LY,
        'Total_BuyValue': Total_BuyValue,
        'Total_BackValue': Total_BackValue,
        'Total_PaidValue': Total_PaidValue,
        'Debt_Queryset': Debt_Queryset,
        'Grant_Old_Debt': Grant_Old_Debt,
        'Grant_BuyValue': Grant_BuyValue,
        'Grant_BackValue': Grant_BackValue,
        'Grant_PaidValue': Grant_PaidValue,
        'Grant_DebtValue': Grant_DebtValue,

    }
    return render(request, 'sales_manage/Customer_Debt/Customer_Debt.html', context)


@login_required
def Customer_Debt_add(request, Customer_id, Year=date.today().year):
    check_row = Customer_Debt.objects.filter(Customer=Customer_id, Year=Year - 1)
    if not check_row.exists():

        Debt_LY = Customer_Debt.objects.filter(Customer=Customer_id, Year=Year - 2)
        Buys = Sales.objects.filter(Customer=Customer_id, year=Year - 1)
        Pays = Customer_Pay.objects.filter(Customer=Customer_id, year=Year - 1)
        Backs = Returned.objects.filter(Customer= Customer_id, year=Year - 1)
        debt = sum(row.Amount for row in Debt_LY)
        Buy = sum(row.Amount for row in Buys)
        Paid = sum(row.Amount for row in Pays)
        Back = sum(row.Amount for row in Backs)
        Debt_Pre_LY = debt + Buy - Paid - Back

        if request.method == 'POST':
            form = customer_debt_form(request.POST)
            if form.is_valid():
                instance = form.save()
                messages.success(request, f'Đã thêm Công Nợ Khách Hàng "{instance.Customer}", Năm: {instance.Year}')
                return redirect(reverse('Customer_Debt', args=[Year]))
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Lỗi: {error}")
        else:
            form = customer_debt_form(initial={'Customer': Customer_id,
                                          'Year': Year - 1,
                                          'Amount': Debt_Pre_LY})

        context = {
            'nav': 'Customer_Debt',
            'form': form,
            'Year': Year,
            'title': 'Thêm: CÔNG NỢ KH',
            'header': 'Thêm Mới: CÔNG NỢ KHÁCH HÀNG'
        }
        return render(request, 'sales_manage/Customer_Debt/Customer_Debt_add.html', context)
    else:
        messages.error(request, 'Công Nợ Này Đã Tồn Tại')
        return Debt(request, year=Year)

@login_required()
def Customer_Debt_update(request, Customer_id, Year=date.today().year):
    check_row = Customer_Debt.objects.filter(Customer=Customer_id, Year=Year - 1)
    if check_row.exists():
        row = Customer_Debt.objects.get(Customer=Customer_id, Year=Year - 1)
        Debt_LY = Customer_Debt.objects.filter(Customer=Customer_id, Year=Year - 2)
        Buys = Sales.objects.filter(Customer=Customer_id, year=Year - 1)
        Pays = Customer_Pay.objects.filter(Customer=Customer_id, year=Year - 1)
        Backs = Returned.objects.filter(Customer=Customer_id, year=Year - 1)
        debt = sum(row.Amount for row in Debt_LY)
        Buy = sum(row.Amount for row in Buys)
        Paid = sum(row.Amount for row in Pays)
        Back = sum(row.Amount for row in Backs)
        Debt_Pre_LY = debt + Buy - Paid - Back

        if request.method == 'POST':
            form = customer_debt_form(request.POST, instance=row)
            if form.is_valid():
                instance = form.save()
                messages.warning(request, f'Đã Sửa Công Nợ Khách Hàng "{instance.Customer}", Năm: {instance.Year}')
                return redirect(reverse('Customer_Debt', args=[Year]))
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Lỗi: {error}")
        else:
            form = customer_debt_form(instance=row, initial={'Amount': Debt_Pre_LY})
            context = {
                'nav': 'debt',
                'form': form,
                'Year': Year,
                'title': 'Sửa: CÔNG NỢ KH',
                'header': 'Sửa: CÔNG NỢ KHÁCH HÀNG'
            }
            return render(request, 'sales_manage/Customer_Debt/Customer_Debt_add.html', context)
    else:
        messages.error(request, 'Công Nợ Chưa Được Tạo')
        return Customer_Debt(request, year=Year)

