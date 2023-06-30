from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import ledger, Transactions
from .forms import ledger_form
from supports.export_excel import export_by_year
import supports.generate_filter as gf
# Create your views here.


@login_required
def export_ledger(request, app='ledger', model='ledger', name='Thu_Chi'):
    return export_by_year(request, app, model, name)


@login_required
def ledger_view_hn(request, year=datetime.now().year, hn=True):
    field_filters = [
        {
            'field_name': 'Date', 'filter_input': request.GET.get('col1_filter'),
            'filter_option': request.GET.get('filter_option_1'), 'related_name': None,
        },
        {
            'field_name': 'Transaction', 'filter_input': request.GET.get('col2_filter'),
            'filter_option': request.GET.get('filter_option_2'), 'related_name': 'R_P',
        },
        {
            'field_name': 'Amount', 'filter_input': request.GET.get('col3_filter'),
            'filter_option': request.GET.get('filter_option_3'), 'related_name': None,
        },
        {
            'field_name': 'Transaction', 'filter_input': request.GET.get('col4_filter'),
            'filter_option': request.GET.get('filter_option_4'), 'related_name': 'Name',
        },
        {
            'field_name': 'Description', 'filter_input': request.GET.get('col5_filter'),
            'filter_option': request.GET.get('filter_option_5'), 'related_name': None,
        },
        {
            'field_name': 'Sync', 'filter_input': request.GET.get('col6_filter'),
            'filter_option': request.GET.get('filter_option_6'), 'related_name': None,
        },
    ]

    filter_query = gf.generate_filter(field_filters)
    try:
        rows = ledger.objects.filter(filter_query, year=year).order_by('Date', 'id')
        if filter_query:
            messages.success(request, 'Lọc Dữ Liệu Thành Công')
    except ValidationError:
        rows = ledger.objects.filter(year=year).order_by('Date', 'id')
        messages.error(request, 'Lỗi: Kiểu Dữ Liệu Lọc Không Hợp Lệ')
    selection_generator = [('1', 'date'), ('2', 'text'), ('3', 'number'), ('4', 'text'), ('5', 'text'),
                           ('6', 'text'),
                           ]
    context = {
        'nav': 'ledger',
        'year': year,
        'hn': hn,
        'rows': rows,
        'selection_generator': selection_generator,
        'RP_Choices': Transactions.RP_Choices,
    }
    return render(request, 'Ledger/Ledger.html', context)


@login_required
def ledger_view(request, year=datetime.now().year):
    return ledger_view_hn(request, year=year, hn=False)


@login_required
def ledger_add(request):
    if request.method == 'POST':
        form = ledger_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            success_message = f'Đã Thêm Giao Dịch Ngày: {instance.Date}; Số Tiền: {instance.Amount}VNĐ,<br>' \
                              f' Hạng Mục: {instance.Transaction}; Diễn Giải: {instance.Description}'
            messages.success(request, mark_safe(success_message))
            return redirect(reverse('ledger_view_hn', args=[instance.year]))
    else:
        form = ledger_form(initial={'Date': datetime.now().date()})
    context = {
        'nav': 'ledger',
        'form': form,
    }
    return render(request, 'Ledger/Ledger_add.html', context)


@login_required
def ledger_delete(request, pk):
    row = ledger.objects.get(id=pk)
    if request.method == 'POST':
        row.delete()
        error_message = f'Đã Xóa Khoản {row.Transaction.R_P}: Ngày {row.Date}, Số Tiền: {row.Amount} VNĐ, <br>'\
                        f'Hạng Mục:{row.Transaction}, Diễn Giải: {row.Description}'
        messages.error(request, mark_safe(error_message))
        return redirect(reverse(ledger_view, args=[row.year]))

    context = {
        'nav': 'ledger',
        'row': row,
    }
    return render(request, 'Ledger/Ledger_delete.html', context)


@login_required
def ledger_update(request, pk):
    row = ledger.objects.get(id=pk)
    if request.method == 'POST':
        form = ledger_form(request.POST, instance=row)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Creator = request.user
            instance.save()
            success_message = f'Đã Sửa Giao Dịch Ngày: {instance.Date}; Số Tiền: {instance.Amount}VNĐ,<br>' \
                              f' Hạng Mục: {instance.Transaction}; Diễn Giải: {instance.Description}'
            messages.success(request, mark_safe(success_message))
            return redirect(reverse('ledger_view_hn', args=[instance.year]))
    else:
        form = ledger_form(instance=row)
    context = {
        'nav': 'ledger',
        'form': form,
    }
    return render(request, 'Ledger/Ledger_update.html', context)
