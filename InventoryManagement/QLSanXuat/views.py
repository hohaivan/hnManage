from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Det_Tay, Tay_Moc, Tay_In, Tay_Nhuom, Cang
from .forms import DetTay_form, TayMoc_form, TayIn_form, TayNhuom_form, In_Cang_form, Nhuom_Cang_form
from supports.export_excel import export_by_year
import supports.generate_filter as gf

# Create your views here.


@login_required
def export_Det_Tay(request, app='QLSanXuat', model='Det_Tay'):
    return export_by_year(request, app, model)

@login_required
def export_Tay_Moc(request, app='QLSanXuat', model='Tay_Moc'):
    return export_by_year(request, app, model)

@login_required
def export_Tay_In(request, app='QLSanXuat', model='Tay_In'):
    return export_by_year(request, app, model)

@login_required
def export_Tay_Nhuom(request, app='QLSanXuat', model='Tay_Nhuom'):
    return export_by_year(request, app, model)

@login_required
def export_Cang(request, app='QLSanXuat', model='Cang'):
    return export_by_year(request, app, model)

@login_required
def WeaveBleach_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'Product_class', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Product_class',
        },
        {
            'field_name': 'Product_name', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': None,
        },
        {
            'field_name': 'M_per_kg', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
        {
            'field_name': 'Fit_size', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': None,
        },
        {
            'field_name': 'Spandex_rate', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': None,
        },
        {
            'field_name': 'FromWhere', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': 'KhoDet',
        },
        {
            'field_name': 'Destination', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': 'KhoTay',
        },
        {
            'field_name': 'BatchID', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'Quantity', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col11_filter'),
            'filter_option': request.GET.get('filter_option_11'), 'related_name': None,
        },
        {
            'field_name': 'CS', 'filter_input': request.GET.get('col12_filter'),
            'filter_option': request.GET.get('filter_option_12'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Det_Tay.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Det_Tay.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ' )
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'number'), ('5', 'number'), ('6', 'number'),
                        ('7', 'text'), ('8', 'text'), ('9', 'text'), ('10', 'number'), ('11', 'number'), ('12', 'number'),
                        ]

    context = {
        'nav': 'weave-bleach',
        'hn': hn,
        'rows': rows,
        'year': year,
        'selection_generator': selection_generator,
    }

    return render(request, 'Production/Det_Tay/Det_Tay.html', context)


@login_required
def WeaveBleach(request, year=datetime.now().year):
    return WeaveBleach_hn(request, year=year, hn=False)


@login_required
def WeaveBleach_add(request):
    if request.method == 'POST':
        form = DetTay_form(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.User_Create = request.user
                instance.save()
                # flash message
                BatchID = instance.BatchID
                messages.success(request, f'Đã thêm thành công mã lô: {BatchID}')
            # empty field
            except IntegrityError:
                # display error message to user
                messages.warning(request, f'Mã lô đã tồn tại, vui lòng xem lại mã lô')
        else:
            messages.error(request, f'Đã Xảy Ra Lỗi, Chưa Thêm Được Thông Tin Lô Hàng !')
    else:
        form = DetTay_form(initial={'Date': datetime.now().date(), 'User_Create': request.user})

    context = {
        'nav': 'weave-bleach',
        'form': form,
    }
    return render(request, 'Production/Det_Tay/Det_Tay_add.html', context)


@login_required
def WeaveBleach_delete(request, pk):
    row = Det_Tay.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        messages.error(request, f'Đã Xóa Mã Lô: {row.BatchID}')
        return redirect(reverse('Det_Tay_hn', args=[row.year]))

    context = {
        'nav': 'weave-bleach',
        'row': row,
    }
    return render(request, 'Production/Det_Tay/Det_Tay_delete.html', context)


@login_required
def WeaveBleach_update(request, pk):
    row = Det_Tay.objects.get(id=pk)
    old_id = row.BatchID

    if request.method == 'POST':
        form = DetTay_form(request.POST, instance=row)
        if form.is_valid():
            try:
                new_instance = form.save(commit=False)
                if not new_instance.User_Create_id:
                    new_instance.User_Create_id = request.user
                new_instance.save(admin=False)
                if old_id == new_instance.BatchID:
                    messages.warning(request, f'Đã Sửa Mã Lô: {row.BatchID}')
                else:
                    messages.warning(request, f'Đã Sửa Mã Lô: {old_id} thành {new_instance.BatchID}')
                return redirect(reverse('Det_Tay_hn', args=[row.year]))
            except IntegrityError:
                messages.error(request, f'Mã Lô Đã Tồn Tại!')
        else:
            messages.error(request, f'Thông tin chỉnh sửa không phù hợp !')
    else:
        form = DetTay_form(instance=row)
    context = {
        'nav': 'weave-bleach',
        'form': form,
        'back_year': row.year,
    }
    return render(request, 'Production/Det_Tay/Det_Tay_update.html', context)


@login_required
def WeaveBleach_detail(request, pk):
    Det = Det_Tay.objects.get(id=pk)
    Moc = Tay_Moc.objects.filter(DetTay_ID=pk).order_by('Date')
    In = Tay_In.objects.filter(DetTay_ID=pk).order_by('Date')
    Nhuom = Tay_Nhuom.objects.filter(DetTay_ID=pk).order_by('Date')

    context = {
        'nav': 'weave-bleach',
        'Det': Det,
        'Moc': Moc,
        'In': In,
        'Nhuom': Nhuom,
    }
    return render(request, 'Production/Det_Tay/detail.html', context)


@login_required
def BleachRaw_hn(request, hn=True, year=datetime.now().year):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Product_class__Product_class',
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': 'Product_name',
        },
        {
            'field_name': 'Customer', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': 'name',
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': 'Destination',
        },
        {
            'field_name': 'Print_Des', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': None,
        },
        {
            'field_name': 'BatchID', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Qty', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Tay_Moc.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Tay_Moc.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'), ('7', 'text'), ('8', 'number'), ('9', 'number'),]
    context = {
        'nav': 'bleach-raw',
        'rows': rows,
        'hn': hn,
        'year': year,
        'selection_generator': selection_generator,
    }
    return render(request, 'Production/Tay_Moc/Tay_Moc.html', context)


@login_required
def BleachRaw(request, hn=False, year=datetime.now().year):
    return BleachRaw_hn(request, hn=hn, year=year)


@login_required
def BleachRaw_add(request, pk):
    row = Det_Tay.objects.get(id=pk)
    if request.method == 'POST':
        form = TayMoc_form(request.POST, initial_foreign_key_value=row)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            messages.success(request, f'Đã Thêm Vào Tẩy-Mộc Mã Lô: {instance.BatchID}')
            return redirect(reverse('Det_Tay_hn', args=[row.year]))
        else:
            messages.error(request, f'Lỗi')
            return redirect(reverse('Tay_Moc_add', args=[row]))
    else:
        form = TayMoc_form(initial_foreign_key_value=row,
                           initial={'Date': datetime.now().date(),
                                    'FromWhere': row.Destination,
                                    'Qty': row.current_stock})

        # Disable the fields
        form.fields['FromWhere'].widget.attrs['disabled'] = True

    context = {
        'nav': 'bleach-raw',
        'form': form,
        'back_year': row.year,
    }
    return render(request, 'Production/Tay_Moc/Tay_Moc_add.html', context)


@login_required
def BleachRaw_delete(request, pk):
    row = Tay_Moc.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        return redirect(reverse('Tay_Moc_hn', args=[row.year]))

    context = {
        'nav': 'bleach-raw',
        'row': row,
    }
    return render(request, 'Production/Tay_Moc/Tay_Moc_delete.html', context)


@login_required
def BleachRaw_update(request, pk):
    row = Tay_Moc.objects.get(id=pk)
    old_id = row.BatchID
    if request.method == 'POST':
        form = TayMoc_form(request.POST, initial_foreign_key_value=row, instance=row)
        old_Qty = row.Qty
        if form.is_valid():
            new_instance = form.save(commit=False)
            if new_instance.Qty > old_Qty + new_instance.DetTay_ID.current_stock:
                messages.error(request, f'Số lượng vượt ngưỡng tồn kho !')
            else:
                new_instance.save(admin=False)
                if old_id == new_instance.BatchID:
                    messages.warning(request, f'Đã Sửa Mã Lô: {row.BatchID}')
                else:
                    messages.warning(request, f'Đã Sửa Mã Lô: {old_id} thành {new_instance.BatchID}')
                return redirect(reverse('Tay_Moc_hn', args=[row.year]))
        else:
            messages.error(request, f'Đã xảy ra lỗi !')
    else:
        form = TayMoc_form(initial_foreign_key_value=row, instance=row)
    context = {
        'nav': 'bleach-raw',
        'form': form,
        'back_year': row.year
    }
    return render(request, 'Production/Tay_Moc/Tay_Moc_update.html', context)


@login_required
def BleachPrint_hn(request, hn=True, year=datetime.now().year):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Product_class__Product_class',
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': 'Product_name',
        },
        {
            'field_name': 'Customer', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': 'name',
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': 'Destination__KhoTay',
        },
        {
            'field_name': 'Print_Des', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': 'KhoIn',
        },
        {
            'field_name': 'BatchID', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Qty', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'CS', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Tay_In.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Tay_In.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'), ('7', 'text'), ('8', 'number'), ('9', 'number'), ('10', 'number'), ]
    context = {
        'nav': 'bleach-print',
        'rows': rows,
        'hn': hn,
        'year': year,
        'selection_generator': selection_generator,
    }
    return render(request, 'Production/Tay_In/Tay_In.html', context)


@login_required
def BleachPrint(request, year=datetime.now().year):
    return BleachPrint_hn(request, year=year, hn=False)


@login_required
def BleachPrint_add(request, pk):
    row = Det_Tay.objects.get(id=pk)
    if request.method == 'POST':
        form = TayIn_form(request.POST, initial_foreign_key_value=row)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            messages.success(request, f'Đã Thêm Vào Tẩy-In Mã Lô: {instance.BatchID}')
            return redirect(reverse('Det_Tay_hn', args=[row.year]))
        else:
            messages.error(request, f'Lỗi')
            return redirect(reverse('Tay_In_add', args=[pk]))

    else:
        form = TayIn_form(initial_foreign_key_value=row,
                          initial={'Date': datetime.now().date(),
                                   'FromWhere': row.Destination,
                                   'Qty': row.current_stock, })

        # Disable the fields
        form.fields['FromWhere'].widget.attrs['disabled'] = True

    context = {
        'nav': 'bleach-print',
        'form': form,
        'back_year': row.year,
    }
    return render(request, 'Production/Tay_In/Tay_In_add.html', context)


@login_required
def BleachPrint_delete(request, pk):
    row = Tay_In.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        return redirect(reverse('Tay_In_hn', args=[row.year]))

    context = {
        'nav': 'bleach-print',
        'row': row,
    }
    return render(request, 'Production/Tay_In/Tay_In_delete.html', context)


@login_required
def BleachPrint_update(request, pk):
    row = Tay_In.objects.get(id=pk)
    old_id = row.BatchID
    if request.method == 'POST':
        form = TayIn_form(request.POST, initial_foreign_key_value=row, instance=row)
        old_Qty = row.Qty
        if form.is_valid():
            new_instance = form.save(commit=False)
            if new_instance.Qty > old_Qty + new_instance.DetTay_ID.current_stock:
                messages.error(request, f'Số lượng vượt ngưỡng tồn kho !')
            else:
                new_instance.save(admin=False)
                if old_id == new_instance.BatchID:
                    messages.warning(request, f'Đã Sửa Mã Lô: {row.BatchID}')
                else:
                    messages.warning(request, f'Đã Sửa Mã Lô: {old_id} thành {new_instance.BatchID}')
                return redirect(reverse('Tay_In_hn', args=[row.year]))
        else:
            messages.error(request, f'Đã xảy ra lỗi !')
    else:
        form = TayIn_form(initial_foreign_key_value=row, instance=row)
    context = {
        'nav': 'bleach-print',
        'form': form,
        'back_year': row.year
    }
    return render(request, 'Production/Tay_In/Tay_In_update.html', context)


@login_required
def BleachDye_hn(request, hn=True, year=datetime.now().year):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'Product_class__Product_class',
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': 'Product_name',
        },
        {
            'field_name': 'Customer', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': 'name',
        },
        {
            'field_name': 'DetTay_ID', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': 'Destination__KhoTay',
        },
        {
            'field_name': 'Dye_Des', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': 'KhoNhuom',
        },
        {
            'field_name': 'BatchID', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Qty', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'CS', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = Tay_Nhuom.objects.filter(filter_query, year=year).order_by('Date')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Tay_Nhuom.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'), ('7', 'text'), ('8', 'number'), ('9', 'number'), ('10', 'number'), ]
    context = {
        'nav': 'bleach-dye',
        'hn': hn,
        'rows': rows,
        'year': year,
        'selection_generator': selection_generator,
    }
    return render(request, 'Production/Tay_Nhuom/Tay_Nhuom.html', context)


@login_required
def BleachDye_add(request, pk):
    row = Det_Tay.objects.get(id=pk)
    if request.method == 'POST':
        form = TayNhuom_form(request.POST, initial_foreign_key_value=row)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            messages.success(request, f'Đã Thêm Vào Tẩy-Nhuộm Mã Lô: {instance.BatchID}')
            return redirect(reverse('Det_Tay_hn', args=[row.year]))
        else:
            messages.error(request, f'Lỗi')
            return redirect(reverse('Tay_Nhuom_add', args=[pk]))
    else:
        form = TayNhuom_form(initial_foreign_key_value=row,
                             initial={'Date': datetime.now().date(),
                                      'FromWhere': row.Destination,
                                      'Qty': row.current_stock, })

        # Disable the fields
        form.fields['FromWhere'].widget.attrs['disabled'] = True

    context = {
        'nav': 'bleach-dye',
        'form': form,
        'back_year': row.year,
    }
    return render(request, 'Production/Tay_Nhuom/Tay_Nhuom_add.html', context)


@login_required
def BleachDye(request, year=datetime.now().year):
    return BleachDye_hn(request, year=year, hn=False)

@login_required
def BleachDye_delete(request, pk):
    row = Tay_Nhuom.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        return redirect(reverse('Tay_Nhuom_hn', args=[row.year]))

    context = {
        'nav': 'bleach-dye',
        'row': row,
    }
    return render(request, 'Production/Tay_Nhuom/Tay_Nhuom_delete.html', context)


@login_required
def BleachDye_update(request, pk):
    row = Tay_Nhuom.objects.get(id=pk)
    old_id = row.BatchID
    if request.method == 'POST':
        form = TayNhuom_form(request.POST, initial_foreign_key_value=row, instance=row)
        old_Qty = row.Qty
        if form.is_valid():
            new_instance = form.save(commit=False)
            if new_instance.Qty > old_Qty + new_instance.DetTay_ID.current_stock:
                messages.error(request, f'Số lượng vượt ngưỡng tồn kho !')
            else:
                new_instance.save(admin=False)
                if old_id == new_instance.BatchID:
                    messages.warning(request, f'Đã Sửa Mã Lô: {row.BatchID}')
                else:
                    messages.warning(request, f'Đã Sửa Mã Lô: {old_id} thành {new_instance.BatchID}')
                return redirect(reverse('Tay_Nhuom_hn', args=[row.year]))
        else:
            messages.error(request, f'Lỗi, thông tin cung cấp không hợp lệ')
            return redirect(reverse('Tay_Nhuom_update', args=[pk]))
    else:
        form = TayNhuom_form(initial_foreign_key_value=row, instance=row, initial={'DetTay_ID': row.DetTay_ID})
    context = {
        'nav': 'bleach-dye',
        'form': form,
        'back_year': row.year,
    }
    return render(request, 'Production/Tay_Nhuom/Tay_Nhuom_update.html', context)


def Stretch_hn(request, hn=True, year=datetime.now().year):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'Product_class', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': None,
        },
        {
            'field_name': 'Product_name', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': None,
        },
        {
            'field_name': 'Product_type', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': None,
        },
        {
            'field_name': 'Print_ID', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': 'Print_Des__KhoIn',
        },
        {
            'field_name': 'Dye_ID', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': 'Dye_Des__KhoNhuom',
        },
        {
            'field_name': 'Dye_Des', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': 'KhoNhuom',
        },
        {
            'field_name': 'BatchID', 'filter_input': request.GET.get('col7_filter'),
            'filter_option': request.GET.get('filter_option_7'), 'related_name': None,
        },
        {
            'field_name': 'Qty', 'filter_input': request.GET.get('col8_filter'),
            'filter_option': request.GET.get('filter_option_8'), 'related_name': None,
        },
        {
            'field_name': 'Weight', 'filter_input': request.GET.get('col9_filter'),
            'filter_option': request.GET.get('filter_option_9'), 'related_name': None,
        },
        {
            'field_name': 'CS', 'filter_input': request.GET.get('col10_filter'),
            'filter_option': request.GET.get('filter_option_10'), 'related_name': None,
        },
    ]
    field_with_noPrintID = [d for i, d in enumerate(field_filters) if i !=4]
    field_with_noDyeID = [d for i, d in enumerate(field_filters) if i !=5]
    query_1 = gf.generate_filter(field_with_noPrintID)
    query_2 = gf.generate_filter(field_with_noDyeID)

    try:
        Queryset1 = Cang.objects.filter(query_1, year=year)
        Queryset2 = Cang.objects.filter(query_2, year=year)
        rows = Queryset1.union(Queryset2).order_by('Date')
        if query_1 or query_2:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = Cang.objects.filter(year=year).order_by('Date')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'text'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'), ('7', 'text'), ('8', 'text'), ('9', 'number'), ('10', 'number'), ]
    context = {
        'nav': 'stretch',
        'hn': hn,
        'rows': rows,
        'year': year,
        'types': Cang.type_choices,
        'selection_generator': selection_generator,
    }
    return render(request, 'Production/Cang/Cang.html', context)


@login_required
def Stretch(request, year=datetime.now().year):
    return Stretch_hn(request, year=year, hn=False)


@login_required
def In_Cang(request, pk):
    row = Tay_In.objects.get(id=pk)
    if request.method == 'POST':
        form = In_Cang_form(request.POST, initial_foreign_key_value=row)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.Creator = request.user
                instance.Product_type = 'P'
                instance.save()
                return redirect(reverse('Tay_In_hn', args=[row.year]))
            except IntegrityError:
                # display error message to user
                messages.warning(request, f'Mã lô đã tồn tại, vui lòng cung cấp mã lô khác')
                # return redirect(reverse('In_Cang_add', args=[pk]))
        else:
            messages.error(request, f'Lỗi, thông tin cung cấp không hợp lệ')
            return redirect(reverse('In_Cang_add', args=[pk]))

    else:
        form = In_Cang_form(initial_foreign_key_value=row,
                            initial={'Date': datetime.now().date(),
                                     'Print_Des': row.Print_Des,
                                     'Qty': row.current_stock,
                                     'Product_type': 'In'})
        # disable fields
        form.fields['Print_Des'].widget.attrs['disabled'] = True
    context = {
        'nav': 'stretch',
        'form': form,
        'back_year': row.year,
    }
    return render(request, 'Production/Cang/In_Cang_add.html', context)


@login_required
def Nhuom_Cang(request, pk):
    row = Tay_Nhuom.objects.get(id=pk)
    if request.method == 'POST':
        form = Nhuom_Cang_form(request.POST, initial_foreign_key_value=row)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.Creator = request.user
                instance.Product_type = 'D'
                instance.save()
                return redirect(reverse('Tay_Nhuom_hn', args=[row.year]))
            except IntegrityError:
                # display error message to user
                messages.warning(request, f'Mã lô đã tồn tại, vui lòng cung cấp mã lô khác')
                # return redirect(reverse('Nhuom_Cang_add', args=[pk]))
        else:
            messages.error(request, f'Lỗi, thông tin cung cấp không hợp lệ')
            return redirect(reverse('Nhuom_Cang_add', args=[pk]))

    else:
        form = Nhuom_Cang_form(initial_foreign_key_value=row,
                               initial={'Date': datetime.now().date(),
                                        'Dye_Des': row.Dye_Des,
                                        'Qty': row.current_stock,
                                        'Product_type': 'Nhuộm'})
        # disable fields
        form.fields['Dye_Des'].widget.attrs['disabled'] = True

    context = {
        'nav': 'stretch',
        'form': form,
        'back_year': row.year,
    }
    return render(request, 'Production/Cang/Nhuom_Cang_add.html', context)


@login_required
def Stretch_delete(request, pk):
    row = Cang.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        return redirect(reverse('Cang_hn', args=[row.year]))

    context = {
        'nav': 'stretch',
        'row': row,
    }
    return render(request, 'Production/Cang/Cang_delete.html', context)


@login_required
def Stretch_update(request, batch):
    row = Cang.objects.get(BatchID=batch)
    if row.Product_type == 'P':
        if request.method == 'POST':
            old_Qty = row.Qty
            form = In_Cang_form(request.POST, initial_foreign_key_value=row, instance=row)
            if form.is_valid():
                new_instance = form.save(commit=False)
                new_instance.Product_type = 'P'
                if new_instance.Qty > old_Qty + new_instance.Print_ID.current_stock:
                    messages.error(request, f'Số lượng vượt ngưỡng tồn kho !')
                else:
                    new_instance.save(admin=False)
                    return redirect(reverse('Cang_hn', args=[row.year]))
            else:
                messages.error(request, f'Lỗi, thông tin cung cấp không hợp lệ')
                return redirect(reverse('Cang_update', args=[batch]))
        else:
            form = In_Cang_form(initial_foreign_key_value=row, instance=row, initial={'Print_Des': row.Print_ID.Print_Des,
                                                                                      'Print_ID': row.Print_ID,
                                                                                      'Product_type': 'In'})
            # disable field
            form.fields['Print_Des'].widget.attrs['disabled'] = True
            form.fields['Print_ID'].required = False
    elif row.Product_type == 'D':
        if request.method == 'POST':
            old_Qty = row.Qty
            form = Nhuom_Cang_form(request.POST, initial_foreign_key_value=row, instance=row)

            if form.is_valid():
                new_instance = form.save(commit=False)
                new_instance.Product_type = 'D'
                if new_instance.Qty > old_Qty + new_instance.Dye_ID.current_stock:
                    messages.error(request, f'Số lượng vượt ngưỡng tồn kho !')
                else:
                    new_instance.save(admin=False)
                    return redirect(reverse('Cang_hn', args=[row.year]))
            else:
                messages.error(request, form.errors)
                return redirect(reverse('Cang_update', args=[batch]))
        else:
            form = Nhuom_Cang_form(initial_foreign_key_value=row, instance=row, initial={'Dye_Des': row.Dye_ID.Dye_Des,
                                                                                         'Dye_ID': row.Dye_ID,
                                                                                         'Product_type': 'Nhuộm',
                                                                                         })

            # disable field
            form.fields['Dye_Des'].widget.attrs['disabled'] = True
    context = {
        'nav': 'stretch',
        'form': form,
        'row': row,
        'back_year': row.year,
    }
    return render(request, 'Production/Cang/Cang_update.html', context)
