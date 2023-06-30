from django.apps import AppConfig


class SaleManageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sale_manage'
    verbose_name = '3. Bán Hàng'

    def ready(self):
        import sale_manage.signals


