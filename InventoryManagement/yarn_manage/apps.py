from django.apps import AppConfig


class YarnManageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yarn_manage'
    verbose_name = '1. Quản Lý Sợi'

    def ready(self):
        import yarn_manage.signals