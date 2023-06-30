from django.contrib import messages
from django.db import IntegrityError
from django.db.models import RestrictedError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from QLSanXuat.models import KhachHang, KhoDet, KhoTay, KhoIn, KhoNhuom, KhoCang, Product_class
from yarn_manage.models import YarnVendor, Warehouse, YarnType
# Create your views here.
from . import forms


@login_required
def Customer_info(request):
    rows = KhachHang.objects.all().order_by('Own', 'id')

    context = {
        'nav': 'Cus_inf',
        'rows': rows,
    }
    return render(request, 'OtherData/Customer_info/Customer_info.html', context)


@login_required
def Customer_add(request):
    if request.method == 'POST':
        form = forms.Customer_form(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Thêm Thành Công Thông Tin Khách Hàng: {instance.name}')
            return redirect(reverse('Customer_info'))
        else:
            messages.error(request, f'Nhập Dự Liệu Không Thành Công')
    else:
        form = forms.Customer_form()
    context = {
        'nav': 'Cus_inf',
        'form': form,
    }
    return render(request, 'OtherData/Customer_info/Customer_add.html', context)


@login_required
def Customer_delete(request, pk):
    row = KhachHang.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.name
            row.delete()
            messages.error(request, f'Đã Xóa Dữ Liệu Khách Hàng: {name}')
            return redirect(reverse('Customer_info'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa Khách Hàng Này')
            return redirect(reverse('Customer_delete', args=[pk]))
    context = {
        'nav': 'Cus_inf',
        'row': row,
    }
    return render(request, 'OtherData/Customer_info/Customer_delete.html', context)


@login_required
def Customer_update(request, pk):
    row = KhachHang.objects.get(id=pk)
    old_name = row.name
    if request.method == 'POST':
        form = forms.Customer_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.name:
                messages.warning(request, f'Đã Sửa Thông Tin Khách Hàng "{inst.name}"')
            else:
                messages.warning(request, f'Đã Sửa Thông Tin & Tên KH: "{old_name}" thành "{inst.name}"')
            return redirect(reverse('Customer_info'))

    else:
        form = forms.Customer_form(instance=row)
    context = {
        'nav': 'Cus_inf',
        'form': form,
    }
    return render(request, 'OtherData/Customer_info/Customer_update.html', context)


@login_required
def WH_OS_ALL(request):
    context = {
        'nav': 'wh_os',
    }
    return render(request, 'OtherData/Warehouse_OutSource/All.html', context)


@login_required
def WH_KhoDet(request):
    rows = KhoDet.objects.all().order_by('OS', 'id')
    context = {
        'nav': 'wh_os',
        'rows': rows,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/1_KhoDet/records.html', context)


@login_required
def WH_KhoDet_add(request):
    if request.method == 'POST':
        form = forms.KhoDet_form(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Đã thêm thành công Kho Dệt: {instance.KhoDet}, Ký Hiệu: {instance.KyHieu}')
            return redirect(reverse('WH_KhoDet'))
    else:
        form = forms.KhoDet_form()
    context = {
        'nav': 'wh_os',
        'form': form,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/1_KhoDet/add.html', context)


@login_required
def WH_KhoDet_delete(request, pk):
    row = KhoDet.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.KhoDet
            row.delete()
            messages.error(request, f'Đã Xóa Xưởng Dệt: {name}')
            return redirect(reverse('WH_KhoDet'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa Xưởng Dệt Này')
            return redirect(reverse('WH_KhoDet_delete', args=[pk]))
    context = {
        'nav': 'wh_os',
        'row': row,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/1_KhoDet/delete.html', context)


@login_required
def WH_KhoDet_update(request, pk):
    row = KhoDet.objects.get(id=pk)
    old_name = row.KhoDet
    if request.method == 'POST':
        form = forms.KhoDet_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.KhoDet:
                messages.warning(request, f'Đã Sửa Thông Tin Xưởng Dệt "{inst.KhoDet}"')
            else:
                messages.warning(request, f'Đã Sửa Xưởng Dệt: "{old_name}" thành "{inst.KhoDet}"')
            return redirect(reverse('WH_KhoDet'))

    else:
        form = forms.KhoDet_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/1_KhoDet/update.html', context)


@login_required
def WH_KhoTay(request):
    rows = KhoTay.objects.all().order_by('OS', 'id')
    context = {
        'nav': 'wh_os',
        'rows': rows,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/2_KhoTay/records.html', context)


@login_required
def WH_KhoTay_add(request):
    if request.method == 'POST':
        form = forms.KhoTay_form(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Đã thêm thành công Lò Tẩy: {instance.KhoTay}, Ký Hiệu: {instance.KyHieu}')
            return redirect(reverse('WH_KhoTay'))
    else:
        form = forms.KhoTay_form()
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoTay'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/2_KhoTay/add.html', context)


@login_required
def WH_KhoTay_delete(request, pk):
    row = KhoTay.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.KhoTay
            row.delete()
            messages.error(request, f'Đã Xóa Lò Tẩy: {name}')
            return redirect(reverse('WH_KhoTay'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa Lò Tẩy Này')
            return redirect(reverse('WH_KhoDet_delete', args=[pk]))
    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_KhoTay'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/2_KhoTay/delete.html', context)


@login_required
def WH_KhoTay_update(request, pk):
    row = KhoTay.objects.get(id=pk)
    old_name = row.KhoTay
    if request.method == 'POST':
        form = forms.KhoTay_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.KhoTay:
                messages.warning(request, f'Đã Sửa Thông Tin Lò Tẩy "{inst.KhoTay}"')
            else:
                messages.warning(request, f'Đã Sửa Lò Tẩy: "{old_name}" thành "{inst.KhoTay}"')
            return redirect(reverse('WH_KhoTay'))

    else:
        form = forms.KhoTay_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoTay'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/2_KhoTay/update.html', context)


@login_required
def WH_KhoIn(request):
    rows = KhoIn.objects.all().order_by('OS', 'id')
    context = {
        'nav': 'wh_os',
        'rows': rows,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/3_KhoIn/records.html', context)


@login_required
def WH_KhoIn_add(request):
    if request.method == 'POST':
        form = forms.KhoIn_form(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Đã thêm thành công Lò In: {instance.KhoIn}, Ký Hiệu: {instance.KyHieu}')
            return redirect(reverse('WH_KhoIn'))
    else:
        form = forms.KhoIn_form()
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoIn'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/3_KhoIn/add.html', context)


@login_required
def WH_KhoIn_delete(request, pk):
    row = KhoIn.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.KhoIn
            row.delete()
            messages.error(request, f'Đã Xóa Lò In: {name}')
            return redirect(reverse('WH_KhoIn'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa Lò In Này')
            return redirect(reverse('WH_KhoIn_delete', args=[pk]))
    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_KhoIn'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/3_KhoIn/delete.html', context)


@login_required
def WH_KhoIn_update(request, pk):
    row = KhoIn.objects.get(id=pk)
    old_name = row.KhoIn
    if request.method == 'POST':
        form = forms.KhoIn_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.KhoIn:
                messages.warning(request, f'Đã Sửa Thông Tin Lò In "{inst.KhoIn}"')
            else:
                messages.warning(request, f'Đã Sửa Lò In: "{old_name}" thành "{inst.KhoIn}"')
            return redirect(reverse('WH_KhoIn'))

    else:
        form = forms.KhoIn_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoIn'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/3_KhoIn/update.html', context)


@login_required
def WH_KhoNhuom(request):
    rows = KhoNhuom.objects.all().order_by('OS', 'id')
    context = {
        'nav': 'wh_os',
        'rows': rows,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/4_KhoNhuom/records.html', context)


@login_required
def WH_KhoNhuom_add(request):
    if request.method == 'POST':
        form = forms.KhoNhuom_form(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Đã thêm thành công Lò Nhuộm: {instance.KhoNhuom}, Ký Hiệu: {instance.KyHieu}')
            return redirect(reverse('WH_KhoNhuom'))
    else:
        form = forms.KhoNhuom_form()
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoNhuom'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/4_KhoNhuom/add.html', context)


@login_required
def WH_KhoNhuom_delete(request, pk):
    row = KhoNhuom.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.KhoNhuom
            row.delete()
            messages.error(request, f'Đã Xóa Lò Nhuộm: {name}')
            return redirect(reverse('WH_KhoNhuom'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa Lò Nhuộm Này')
            return redirect(reverse('WH_KhoNhuom_delete', args=[pk]))
    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_KhoNhuom'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/4_KhoNhuom/delete.html', context)


@login_required
def WH_KhoNhuom_update(request, pk):
    row = KhoNhuom.objects.get(id=pk)
    old_name = row.KhoNhuom
    if request.method == 'POST':
        form = forms.KhoNhuom_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.KhoNhuom:
                messages.warning(request, f'Đã Sửa Thông Tin Lò Nhuộm "{inst.KhoNhuom}"')
            else:
                messages.warning(request, f'Đã Sửa Lò Nhuộm: "{old_name}" thành "{inst.KhoNhuom}"')
            return redirect(reverse('WH_KhoNhuom'))

    else:
        form = forms.KhoNhuom_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoNhuom'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/4_KhoNhuom/update.html', context)


@login_required
def WH_KhoCang(request):
    rows = KhoCang.objects.all().order_by('OS', 'id')
    context = {
        'nav': 'wh_os',
        'rows': rows,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/5_KhoCang/records.html', context)


@login_required
def WH_KhoCang_add(request):
    if request.method == 'POST':
        form = forms.KhoCang_form(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Đã thêm thành công Lò Căng: {instance.KhoCang}, Ký Hiệu: {instance.KyHieu}')
            return redirect(reverse('WH_KhoCang'))
    else:
        form = forms.KhoCang_form()
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoCang'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/5_KhoCang/add.html', context)


@login_required
def WH_KhoCang_delete(request, pk):
    row = KhoCang.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.KhoCang
            row.delete()
            messages.error(request, f'Đã Xóa Lò Căng: {name}')
            return redirect(reverse('WH_KhoCang'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa Lò Căng Này')
            return redirect(reverse('WH_KhoCang_delete', args=[pk]))
    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_KhoCang'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/5_KhoCang/delete.html', context)


@login_required
def WH_KhoCang_update(request, pk):
    row = KhoCang.objects.get(id=pk)
    old_name = row.KhoCang
    if request.method == 'POST':
        form = forms.KhoCang_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.KhoCang:
                messages.warning(request, f'Đã Sửa Thông Tin Lò Căng "{inst.KhoCang}"')
            else:
                messages.warning(request, f'Đã Sửa Lò Căng: "{old_name}" thành "{inst.KhoCang}"')
            return redirect(reverse('WH_KhoCang'))

    else:
        form = forms.KhoCang_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_KhoCang'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/5_KhoCang/update.html', context)


@login_required
def WH_ProductType(request):
    rows = Product_class.objects.all().order_by('id')

    if request.method == 'POST':
        form = forms.ProductClass_form(request.POST)
        if form.is_valid():
            ins = form.save()
            messages.success(request, f'Lưu Thành Công Phân Loại Hàng: "{ins.Product_class}"')
    else:
        form = forms.ProductClass_form()
    context = {
        'nav': 'wh_os',
        'rows': rows,
        'form': form,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/6_ProductType/ProductType.html', context)


@login_required
def WH_ProductType_delete(request, pk):
    row = Product_class.objects.get(id=pk)

    if request.method == 'POST':
        try:
            name = row.Product_class
            row.delete()
            messages.success(request, f'Đã Xóa Phân Loại Hàng "{name}"')
            return redirect(reverse('WH_ProductType'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa "{name}"')
            return redirect(reverse('WH_ProductType_delete', args=[pk]))

    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_ProductType'
    }

    return render(request, 'OtherData/Warehouse_OutSource/Production/6_ProductType/delete.html', context)


@login_required
def WH_ProductType_update(request, pk):
    row = Product_class.objects.get(id=pk)
    old_name = row.Product_class
    if request.method == 'POST':
        form = forms.ProductClass_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            messages.warning(request, f'Đã Sửa Phân Loại Hàng: "{old_name}" thành "{inst.Product_class}"')
            return redirect(reverse('WH_ProductType'))

    else:
        form = forms.ProductClass_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_ProductType'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Production/6_ProductType/update.html', context)


@login_required
def WH_YarnVendor(request):
    rows = YarnVendor.objects.all().order_by('Code')
    context = {
        'nav': 'wh_os',
        'rows': rows,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/1_Vendor/records.html', context)


@login_required
def WH_YarnVendor_add(request):
    if request.method == 'POST':
        form = forms.YarnVendor_form(request.POST)
        if form.is_valid():
            ins = form.save()
            messages.success(request, f'Lưu Thành Công Người Bán "{ins.Name}", Mã NBH: {ins.VendorCode}')
            return redirect(reverse('WH_YarnVendor'))
    else:
        form = forms.YarnVendor_form()

    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_YarnVendor'
    }

    return render(request, 'OtherData/Warehouse_OutSource/Yarn/1_Vendor/add.html', context)


@login_required
def WH_YarnVendor_delete(request, pk):
    row = YarnVendor.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.Name
            row.delete()
            messages.error(request, f'Đã Xóa NCC Sợi "{name}"')
            return redirect(reverse('WH_YarnVendor'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa NCC Sợi Này')
            return redirect(reverse('WH_YarnVendor_delete', args=[pk]))
    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_YarnVendor'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/1_Vendor/delete.html', context)


@login_required
def WH_YarnVendor_update(request, pk):
    row = YarnVendor.objects.get(id=pk)
    old_name = row.Name
    if request.method == 'POST':
        form = forms.YarnVendor_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.Name:
                messages.warning(request, f'Đã Sửa Thông Tin NCC Sợi "{inst.Name}"')
            else:
                messages.warning(request, f'Đã Sửa NCC Sợi "{old_name}" thành "{inst.Name}"')
            return redirect(reverse('WH_YarnVendor'))

    else:
        form = forms.YarnVendor_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_YarnVendor'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/1_Vendor/update.html', context)


@login_required
def WH_Warehouse(request):
    rows = Warehouse.objects.all().order_by('id')
    context = {
        'nav': 'wh_os',
        'rows': rows,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/2_Warehouse/records.html', context)


@login_required
def WH_Warehouse_add(request):
    if request.method == 'POST':
        form = forms.Warehouse_form(request.POST)
        if form.is_valid():
            ins = form.save()
            messages.success(request, f'Lưu Thành Công Kho Sợi "{ins.Name}", Ký Hiệu: {ins.Code}')
            return redirect(reverse('WH_Warehouse'))
    else:
        form = forms.Warehouse_form()

    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_Warehouse'
    }

    return render(request, 'OtherData/Warehouse_OutSource/Yarn/2_Warehouse/add.html', context)


@login_required
def WH_Warehouse_delete(request, pk):
    row = Warehouse.objects.get(id=pk)
    if request.method == 'POST':
        try:
            name = row.Name
            row.delete()
            messages.error(request, f'Đã Xóa Kho Sợi "{name}"')
            return redirect(reverse('WH_Warehouse'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa Kho Sợi Này')
            return redirect(reverse('WH_Warehouse_delete', args=[pk]))
    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_Warehouse'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/2_Warehouse/delete.html', context)


@login_required
def WH_Warehouse_update(request, pk):
    row = Warehouse.objects.get(id=pk)
    old_name = row.Name
    if request.method == 'POST':
        form = forms.Warehouse_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            if old_name == inst.Name:
                messages.warning(request, f'Đã Sửa Thông Tin Kho Sợi "{inst.Name}"')
            else:
                messages.warning(request, f'Đã Sửa Kho Sợi "{old_name}" thành "{inst.Name}"')
            return redirect(reverse('WH_Warehouse'))

    else:
        form = forms.Warehouse_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_Warehouse'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/2_Warehouse/update.html', context)


@login_required
def WH_YarnType(request):
    rows = YarnType.objects.all().order_by('id')

    if request.method == 'POST':
        form = forms.YarnType_form(request.POST)
        if form.is_valid():
            ins = form.save()
            messages.success(request, f'Lưu Thành Công Loại Sợi: "{ins.Name}"')
    else:
        form = forms.YarnType_form()
    context = {
        'nav': 'wh_os',
        'rows': rows,
        'form': form,
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/3_YarnType/YarnType.html', context)


@login_required
def WH_YarnType_delete(request, pk):
    row = YarnType.objects.get(id=pk)

    if request.method == 'POST':
        try:
            name = row.Name
            row.delete()
            messages.success(request, f'Đã Xóa Loại Sợi "{name}"')
            return redirect(reverse('WH_YarnType'))
        except RestrictedError:
            messages.error(request, f'Không Thể Xóa "{name}"')
            return redirect(reverse('WH_YarnType_delete', args=[pk]))

    context = {
        'nav': 'wh_os',
        'row': row,
        'back_link': 'WH_YarnType'
    }

    return render(request, 'OtherData/Warehouse_OutSource/Yarn/3_YarnType/delete.html', context)


@login_required
def WH_YarnType_update(request, pk):
    row = YarnType.objects.get(id=pk)
    old_name = row.Name
    if request.method == 'POST':
        form = forms.YarnType_form(request.POST, instance=row)
        if form.is_valid():
            inst = form.save()
            messages.warning(request, f'Đã Sửa Loại Sợi: "{old_name}" thành "{inst.Name}"')
            return redirect(reverse('WH_YarnType'))

    else:
        form = forms.YarnType_form(instance=row)
    context = {
        'nav': 'wh_os',
        'form': form,
        'back_link': 'WH_YarnType'
    }
    return render(request, 'OtherData/Warehouse_OutSource/Yarn/3_YarnType/update.html', context)
