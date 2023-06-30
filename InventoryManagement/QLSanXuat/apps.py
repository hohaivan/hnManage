from django.apps import AppConfig


class QlsanxuatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'QLSanXuat'
    verbose_name = '2. Sản Xuất'

    def ready(self):
        import QLSanXuat.signals
