from django.db import models

# Create your models here.

class spandex_default_rate(models.Model):
    spandex_rate = models.DecimalField(max_digits=3, decimal_places=1)

    def save(self, sd=None, *args, **kwargs):
        if sd:
            self.spandex_rate = sd
        if self.pk != 1:
            pass
        else:
            super().save(*args, **kwargs)
