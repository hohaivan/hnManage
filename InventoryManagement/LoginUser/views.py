from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'Site_login/site_login.html'
    success_url = reverse_lazy('main_page')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST, label_suffix='')
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mật Khẩu Của Bạn Thay Đổi Thành Công, Vui Lòng Đăng Nhập Lại')
            return redirect('user-logout')

    else:
        form = PasswordChangeForm(request.user, label_suffix='')

    form.fields['old_password'].label = 'Mật Khẩu Cũ: '
    form.fields['new_password1'].label = 'Mật Khẩu Mới: '
    form.fields['new_password2'].label = 'Nhập Lại Mật Khẩu Mới: '

    return render(request, 'Site_login/ChangePassword.html', {'form': form})



