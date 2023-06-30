from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, DecimalField, Subquery, OuterRef, Max
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from datetime import datetime, date
from .models import YarnOrder, Delivery, YarnPay, YarnVendor, YarnDebt_LY, YarnTransfer
from .forms import YarnOrder_form, Delivery_form, YarnPay_form, YarnTransfer_form, YarnDebt_form
from supports.export_excel import export_by_year, export_to_excel, get_model_by_name
import supports.generate_filter as gf

# Create your views here.
@login_required
def export_YarnOrder(request, app='yarn_manage', model='YarnOrder'):
    return export_by_year(request, app, model, name='Dat_Soi')

@login_required
def export_Delivery(request, app='yarn_manage', model='Delivery'):
    return export_by_year(request, app, model, name='Giao_Soi')

@login_required
def export_Transfer(request, app='yarn_manage', model='YarnTransfer'):
    return export_by_year(request, app, model, name='Xuat_Nhap_Soi')

@login_required
def export_YarnPay(request, app='yarn_manage', model='YarnPay'):
    return export_by_year(request, app, model, name='Tra_Tien_Soi')

@login_required
def export_YarnDebt(request):
    app_label = 'yarn_manage'
    model_name = 'YarnDebt_LY'
    year = request.GET.get('year')
    Model = get_model_by_name(app_label, model_name)
    if Model is not None:
        filter_params = {'Year': year}
        order_by = ['Vendor']
        filename = f'Cong_No_Soi_{year}_at_{datetime.today().date()}.xlsx'
        return export_to_excel(request, Model, filter_params, order_by, filename)
    else:
        raise ValueError("Model not found.")


@login_required
def order_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'Vendor', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Name',
        },
        {
            'field_name': 'YarnType', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': None,
        },
        {
            'field_name': 'YarnStats', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
        {
            'field_name': 'YarnCode', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': None,
        },
        {
            'field_name': 'BoxQty', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': None,
        },
        {
            'field_name': 'Box_Pack', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Price', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'Amount', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
        {
            'field_name': 'BatchID', 'filter_input': request.GET.get('col11_filter'),
            'filter_option': request.GET.get('filter_option_11'), 'related_name': None,
        },
        {
            'field_name': 'Rest_B', 'filter_input': request.GET.get('col12_filter'),
            'filter_option': request.GET.get('filter_option_12'), 'related_name': None,
        },
        {
            'field_name': 'Rest_W', 'filter_input': request.GET.get('col13_filter'),
            'filter_option': request.GET.get('filter_option_13'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = YarnOrder.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = YarnOrder.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'number'), ('7', 'text'), ('8', 'number'), ('9', 'number'),
                           ('10', 'number'), ('11', 'text'), ('12', 'number'), ('13', 'number')]
    context = {
        'nav': 'yarn_order',
        'hn': hn,
        'year': year,
        'rows': rows,
        'pack_types': YarnOrder.Package_choice,
        'selection_generator': selection_generator,
    }
    return render(request, 'Yarn/Order/Order.html', context)


@login_required
def order(request, year=datetime.now().year):
    return order_hn(request, year=year, hn=False)


@login_required
def order_add(request):
    if request.method == 'POST':
        form = YarnOrder_form(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.Creator = request.user
                instance.save()
                # flash messages
                BatchID = instance.BatchID
                messages.success(request, f'Đã thêm thành công mã lô: {BatchID}')
                return redirect(reverse('yarn_order_hn', args=[instance.year]))
            except IntegrityError:
                messages.warning(request, f'Mã lô đã tồn tại, vui lòng xem lại mã lô')
        else:
            messages.error(request, f'Đã Xảy Ra Lỗi, Chưa Thêm Được Thông Tin Lô Hàng !')
    else:
        form = YarnOrder_form(initial={'Date': datetime.now().date()})
    context = {
        'nav': 'yarn_order',
        'form': form,
    }
    return render(request, 'Yarn/Order/Order_add.html', context)


@login_required
def order_delete(request, pk):
    row = YarnOrder.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        return redirect(reverse('yarn_order_hn', args=[row.year]))

    context = {
        'nav': 'yarn_order',
        'row': row,
        'Time': row.Created_Time.strftime('%d-%m-%Y lúc %H:%M:%S'),
    }
    return render(request, 'Yarn/Order/Order_delete.html', context)


@login_required
def order_update(request, pk):
    row = YarnOrder.objects.get(id=pk)
    if request.method == 'POST':
        form = YarnOrder_form(request.POST, instance=row)
        if form.is_valid():
            new_instance = form.save(commit=False)
            if not new_instance.Creator_id:
                new_instance.Creator_id = request.user
            new_instance.save()
            return redirect(reverse('yarn_order_hn', args=[row.year]))
        else:
            messages.error(request, f'Chỉnh Sửa Không Thành Công')
    else:
        form = YarnOrder_form(instance=row)

    context = {
        'nav': 'yarn_order',
        'row': row,
        'form': form,
    }
    return render(request, 'Yarn/Order/Order_update.html', context)


@login_required
def delivery_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'OrderID', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Vendor__Name',
        },
        {
            'field_name': 'OrderID', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': 'YarnType',
        },
        {
            'field_name': 'OrderID', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': 'YarnStats',
        },
        {
            'field_name': 'YarnCode', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': None,
        },
        {
            'field_name': 'BoxQty', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': None,
        },
        {
            'field_name': 'OrderID', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': 'Box_Pack',
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Price', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'OtherCost', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
        {
            'field_name': 'PayVue', 'filter_input': request.GET.get('col11_filter'),
            'filter_option': request.GET.get('filter_option_11'), 'related_name': None,
        },
        {
            'field_name': 'OrderID', 'filter_input': request.GET.get('col12_filter'),
            'filter_option': request.GET.get('filter_option_12'), 'related_name': 'BatchID',
        },
        {
            'field_name': 'Warehouse', 'filter_input': request.GET.get('col13_filter'),
            'filter_option': request.GET.get('filter_option_13'), 'related_name': None,
        },
        {
            'field_name': 'Sync', 'filter_input': request.GET.get('col14_filter'),
            'filter_option': request.GET.get('filter_option_14'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Delivery.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Delivery.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'number'), ('7', 'text'), ('8', 'number'), ('9', 'number'),
                           ('10', 'number'), ('11', 'number'), ('12', 'text'), ('13', 'text'), ('14', 'text')]
    context = {
        'nav': 'yarn_delivery',
        'hn': hn,
        'year': year,
        'rows': rows,
        'pack_types': YarnOrder.Package_choice,
        'selection_generator': selection_generator,
    }
    return render(request, 'Yarn/Delivery/Delivery.html', context)


@login_required
def delivery(request, year=datetime.now().year):
    return delivery_hn(request, year=year, hn=False)


@login_required
def delivery_add(request, pk):
    row = YarnOrder.objects.get(id=pk)
    if request.method == 'POST':
        form = Delivery_form(request.POST, initial_foreign_key_value=row)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.Creator = request.user
                instance.save()
                # flash messages
                messages.success(request,
                                 f'Đã Thêm Thành Công GIAO SỢI Lô: {instance.OrderID}| Ngày: {instance.Date}| Từ: {instance.OrderID.Vendor}| Đến: {instance.Warehouse}')
                return redirect(reverse('yarn_order_hn', args=[instance.year]))
            except IntegrityError:
                messages.warning(request, f'Lần Giao Này Đã Tồn Tại')
        else:
            messages.error(request, f'Lưu Dữ Liệu Không Thành Công')

        return redirect(reverse('yarn_delivery_add', args=[pk]))

    else:
        form = Delivery_form(initial_foreign_key_value=row, initial={'Date': datetime.now().date(),
                                                                     'Vendor': row.Vendor.Name,
                                                                     'YarnType': row.YarnType,
                                                                     'YarnStats': row.YarnStats,
                                                                     'YarnCode': row.YarnCode,
                                                                     'Box_Pack': row.get_Box_Pack_display,
                                                                     'Price': row.Price,
                                                                     })
    context = {

        'nav': 'yarn_delivery',
        'row': row,
        'form': form,
    }
    return render(request, 'Yarn/Delivery/Delivery_add.html', context)


@login_required
def delivery_delete(request, pk):
    row = Delivery.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        return redirect(reverse('yarn_delivery_hn', args=[row.year]))

    context = {
        'nav': 'yarn_order',
        'row': row,
        'rowID': row.OrderID,
    }
    return render(request, 'Yarn/Delivery/Delivery_delete.html', context)


@login_required
def delivery_update(request, pk):
    row = Delivery.objects.get(id=pk)
    if request.method == 'POST':
        form = Delivery_form(request.POST, initial_foreign_key_value=row, instance=row)
        if form.is_valid():
            new_instance = form.save(commit=False)
            if not new_instance.Creator_id:
                new_instance.Creator_id = request.user
            new_instance.save()
            messages.warning(request,
                             f'Sửa Thành Công Giao Sợi Ngày: {new_instance.Date}, Lô: {new_instance.OrderID.BatchID}, Đến: {row.Warehouse} ')
            return redirect(reverse('yarn_delivery_hn', args=[row.year]))
        else:
            messages.error(request, f'Chỉnh Sửa Không Thành Công')
    else:
        form = Delivery_form(initial_foreign_key_value=row, initial={'Vendor': row.OrderID.Vendor.Name,
                                                                     'YarnType': row.OrderID.YarnType,
                                                                     'YarnStats': row.OrderID.YarnStats,
                                                                     'YarnCode': row.YarnCode,
                                                                     'Box_Pack': row.OrderID.get_Box_Pack_display,
                                                                     'Price': row.Price,
                                                                     }, instance=row)
    context = {
        'nav': 'yarn_order',
        'row': row,
        'form': form,
    }
    return render(request, 'Yarn/Delivery/Delivery_update.html', context)


@login_required
def transfer_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'YarnType', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Name',
        },
        {
            'field_name': 'YarnStats', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': None,
        },
        {
            'field_name': 'YarnCode', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
        {
            'field_name': 'Origin', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': 'Name__Name',
        },
        {
            'field_name': 'Destination', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': 'Name',
        },
        {
            'field_name': 'BoxQty', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Box_Pack', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'Sync', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = YarnTransfer.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = YarnTransfer.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'), ('7', 'number'), ('8', 'text'), ('9', 'number'),
                           ('10', 'text'),]
    context = {
        'nav': 'yarn_transfer',
        'hn': hn,
        'year': year,
        'rows': rows,
        'pack_types': YarnOrder.Package_choice,
        'selection_generator': selection_generator,
    }
    return render(request, 'Yarn/Transfer/Transfer.html', context)


@login_required
def transfer(request, year=datetime.now().year):
    return transfer_hn(request, year=year, hn=False)


@login_required
def transfer_add(request):
    if request.method == 'POST':
        form = YarnTransfer_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            # flash messages
            messages.success(request,
                            f'Đã thêm Xuất Nhập Sợi {instance.YarnType} từ "{instance.Origin}", '
                            f'đến "{instance.Destination}" vào {instance.Date}')
            return redirect(reverse('yarn_transfer_hn', args=[instance.year]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Lỗi: {error}")
    else:
        form = YarnTransfer_form(initial={'Date': datetime.now().date()})
    context = {
        'nav': 'yarn_transfer',
        'form': form,
    }
    return render(request, 'Yarn/Transfer/Transfer_add.html', context)


@login_required
def transfer_delete(request, pk):
    row = YarnTransfer.objects.get(id=pk)
    if request.method == 'POST':
        row.delete(Signal=False)
        return redirect(reverse('yarn_transfer_hn', args=[row.year]))

    context = {
        'nav': 'yarn_transfer',
        'row': row,
    }
    return render(request, 'Yarn/Transfer/Transfer_delete.html', context)


@login_required
def transfer_update(request, pk):
    row = YarnTransfer.objects.get(id=pk)
    if request.method == 'POST':
        form = YarnTransfer_form(request.POST, instance=row)
        if form.is_valid():
            new_instance = form.save(commit=False)
            if not new_instance.Creator_id:
                new_instance.Creator_id = request.user
            new_instance.save()
            return redirect(reverse('yarn_transfer_hn', args=[row.year]))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Lỗi: {error}")
    else:
        form = YarnTransfer_form(instance=row)

    context = {
        'nav': 'yarn_order',
        'row': row,
        'form': form,
    }
    return render(request, 'Yarn/Transfer/Transfer_update.html', context)


@login_required
def Yarn_Pay_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'Vendor', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Name',
        },
        {
            'field_name': 'Vendor', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': 'Vendor_Code',
        },
        {
            'field_name': 'Pay', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
        {
            'field_name': 'Deposit', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': 'Name__Name',
        },
        {
            'field_name': 'Batch', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': 'Name',
        },
        {
            'field_name': 'Sync', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = YarnPay.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = YarnPay.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'number'), ('5', 'number'),
                           ('6', 'text'), ('7', 'text'),]
    context = {
        'nav': 'yarn_pay',
        'year': year,
        'hn': hn,
        'rows': rows,
        'selection_generator': selection_generator,
    }
    return render(request, 'Yarn/Payment/YarnPay.html', context)


@login_required
def Yarn_Pay(request, year=datetime.now().year):
    return Yarn_Pay_hn(request, year=year, hn=False)


@login_required
def Yarn_Pay_add(request):
    if request.method == 'POST':
        form = YarnPay_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            # flash messages
            messages.success(request,
                             f'Đã Lưu Trả Tiền Sợi Ngày "{instance.Date}", Trả Cho "{instance.Vendor}", Số Tiền: {instance.Pay}')
            return redirect(reverse('yarn_pay_hn', args=[instance.year]))

        else:
            messages.error(request, f'Đã Xảy Ra Lỗi, Chưa Thêm Được Thông Tin Trả Tiền Sợi !')
    else:
        form = YarnPay_form(initial={'Date': datetime.now().date()})

    context = {
        'nav': 'yarn_pay',
        'form': form,
    }
    return render(request, 'Yarn/Payment/YarnPay_add.html', context)


@login_required
def Yarn_Pay_delete(request, pk):
    row = YarnPay.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        messages.error(request, f'Đã Xóa Trả Tiền Sợi Ngày "{row.Date}", Trả Cho "{row.Vendor}", Số Tiền: {row.Pay}')
        return redirect(reverse('yarn_pay_hn', args=[row.year]))

    context = {
        'nav': 'yarn_pay',
        'row': row,
    }
    return render(request, 'Yarn/Payment/YarnPay_delete.html', context)


@login_required
def Yarn_Pay_update(request, pk):
    row = YarnPay.objects.get(id=pk)
    if request.method == 'POST':
        form = YarnPay_form(request.POST, instance=row)
        if form.is_valid:
            form.save()
            return redirect(reverse('yarn_pay_hn', args=[row.year]))
    else:
        form = YarnPay_form(instance=row)

    context = {
        'nav': 'yarn_pay',
        'row': row,
        'form': form,
    }
    return render(request, 'Yarn/Payment/YarnPay_update.html', context)


@login_required
def Yarn_Debt(request, year=datetime.now().year):
    filter_date = request.GET.get('filter_date', date.today())

    rows = YarnVendor.objects.all().order_by('VendorCode')
    debt_LY = YarnDebt_LY.objects.filter(Year=year - 1)
    Total_BuyValue = Delivery.objects.filter(year=year, Date__lte=filter_date).values(
        'OrderID__Vendor__Name').annotate(BuyValue=Sum('PayValue'), Last_Delivery=Max('Date'))
    Total_PaidValue = YarnPay.objects.filter(year=year, Date__lte=filter_date).values(
        'Vendor__Name').annotate(PaidValue=Sum('Pay'), Last_Paid=Max('Date'))

    # Join the two querysets using a subquery expression
    Vendor_Queryset = YarnVendor.objects.annotate(
        amount_old_debt=Coalesce(Subquery(
            debt_LY.filter(Vendor=OuterRef('pk')).values('Debt')[:1],
            output_field=DecimalField()
        ), Decimal(0)),
        amount_bought_in=Coalesce(Subquery(
            Total_BuyValue.filter(OrderID__Vendor=OuterRef('pk')).values('BuyValue')[:1],
            output_field=DecimalField()
        ), Decimal(0)),
        amount_paid=Coalesce(Subquery(
            Total_PaidValue.filter(Vendor=OuterRef('pk')).values('PaidValue')[:1],
            output_field=DecimalField()
        ), Decimal(0)),
    )

    # Then you can annotate the vendor queryset with the debt value
    Debt_Queryset = Vendor_Queryset.annotate(
        debt_value=F('amount_old_debt', ) + F('amount_bought_in') - F('amount_paid'))

    # Aggregates
    Grant_Old_Debt = debt_LY.aggregate(Sum('Debt'))
    Grant_BuyValue = Total_BuyValue.aggregate(Sum('BuyValue'))
    Grant_PaidValue = Total_PaidValue.aggregate(Sum('PaidValue'))
    Grant_DebtValue = Debt_Queryset.aggregate(Sum('debt_value'))
    context = {
        'nav': 'debt',
        'filter_date': filter_date,
        'year': year,
        'last_year': year - 1,
        'rows': rows,
        'debt_LY': debt_LY,
        'Total_BuyValue': Total_BuyValue,
        'Total_PaidValue': Total_PaidValue,
        'Debt_Queryset': Debt_Queryset,
        'Grant_Old_Debt': Grant_Old_Debt,
        'Grant_BuyValue': Grant_BuyValue,
        'Grant_PaidValue': Grant_PaidValue,
        'Grant_DebtValue': Grant_DebtValue,

    }

    return render(request, 'Yarn/Debt/YarnDebt.html', context)


@login_required
def Yarn_Debt_add(request, Vendor_id, Year=date.today().year):
    check_row = YarnDebt_LY.objects.filter(Vendor=Vendor_id, Year=Year-1)
    if not check_row.exists():

        Debt_LY = YarnDebt_LY.objects.filter(Vendor=Vendor_id, Year=Year-2)
        Buys = Delivery.objects.filter(OrderID__Vendor__id=Vendor_id, year=Year-1)
        Pays = YarnPay.objects.filter(Vendor=Vendor_id, year=Year-1)
        debt = sum(row.Debt for row in Debt_LY)
        Buy = sum(row.PayValue for row in Buys)
        Pay = sum(row.Pay for row in Pays)
        Debt_Pre_LY = debt + Buy - Pay

        if request.method == 'POST':
            form = YarnDebt_form(request.POST)
            if form.is_valid():
                instance = form.save()
                messages.success(request, f'Đã thêm Công Nợ Người Bán "{instance.Vendor}", Năm: {instance.Year}')
                return redirect(reverse('yarn_debt', args=[Year]))
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Lỗi: {error}")
        else:
            form = YarnDebt_form(initial={'Vendor': Vendor_id,
                                          'Year': Year-1,
                                          'Debt': Debt_Pre_LY})

        context = {
            'nav': 'debt',
            'form': form,
            'Year': Year,
            'title': 'Thêm: CÔNG NỢ SỢI',
            'header': 'Thêm Mới: CÔNG NỢ SỢI',
        }
        return render(request, 'Yarn/Debt/YarnDebt_add.html', context)
    else:
        messages.error(request, 'Công Nợ Này Đã Tồn Tại')
        return Yarn_Debt(request, year=Year)


@login_required
def Yarn_Debt_update(request, Vendor_id, Year=date.today().year):
    check_row = YarnDebt_LY.objects.filter(Vendor=Vendor_id, Year=Year-1)
    if check_row.exists():
        row = YarnDebt_LY.objects.get(Vendor=Vendor_id, Year=Year-1)
        Debt_LY = YarnDebt_LY.objects.filter(Vendor=Vendor_id, Year=Year-2)
        Buys = Delivery.objects.filter(OrderID__Vendor__id=Vendor_id, year=Year-1)
        Pays = YarnPay.objects.filter(Vendor=Vendor_id, year=Year-1)
        debt = sum(row.Debt for row in Debt_LY)
        Buy = sum(row.PayValue for row in Buys)
        Pay = sum(row.Pay for row in Pays)
        Debt_Pre_LY = debt + Buy - Pay

        if request.method == 'POST':
            form = YarnDebt_form(request.POST, instance=row)
            if form.is_valid():
                instance = form.save()
                messages.warning(request, f'Đã Sửa Công Nợ Người Bán "{instance.Vendor}", Năm: {instance.Year}')
                return redirect(reverse('yarn_debt', args=[Year]))
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Lỗi: {error}")
        else:
            form = YarnDebt_form(instance=row, initial={'Debt': Debt_Pre_LY})
            context = {
                'nav': 'debt',
                'form': form,
                'Year': Year,
                'title': 'Sửa: CÔNG NỢ SỢI',
                'header': 'Sửa: CÔNG NỢ SỢI',
            }
            return render(request, 'Yarn/Debt/YarnDebt_add.html', context)
    else:
        messages.error(request, 'Công Nợ Chưa Được Tạo')
        return Yarn_Debt(request, year=Year)
