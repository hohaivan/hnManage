from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Det_Tay, Tay_In, Tay_Moc, Tay_Nhuom, Cang


# update ton kho Det Tay
@receiver(post_save, sender=Tay_Moc)
def post_save_Tay_Moc(sender, instance, created, **kwargs):
    obj = Det_Tay.objects.get(BatchID=instance.DetTay_ID)
    obj.save()

@receiver(post_save, sender=Tay_In)
def post_save_Tay_In(sender, instance, created, **kwargs):
    obj = Det_Tay.objects.get(BatchID=instance.DetTay_ID)
    obj.save()

@receiver(post_save, sender=Tay_Nhuom)
def post_save_Tay_Nhuom(sender, instance, created, **kwargs):
    obj = Det_Tay.objects.get(BatchID=instance.DetTay_ID)
    obj.save()

@receiver(post_delete, sender=Tay_Moc)
def post_del_Tay_Moc(sender, instance, **kwargs):
    obj = Det_Tay.objects.get(BatchID=instance.DetTay_ID)
    obj.save()

@receiver(post_delete, sender=Tay_In)
def post_del_Tay_In(sender, instance, **kwargs):
    obj = Det_Tay.objects.get(BatchID=instance.DetTay_ID)
    obj.save()

@receiver(post_delete, sender=Tay_Nhuom)
def post_del_Tay_Nhuom(sender, instance, **kwargs):
    obj = Det_Tay.objects.get(BatchID=instance.DetTay_ID)
    obj.save()

# update ton kho Tay In Tay Nhuom
@receiver(post_save, sender=Cang)
def post_save_Cang(sender, instance, **kwargs):
    if instance.Product_type == 'P':
        obj = Tay_In.objects.get(BatchID=instance.Print_ID)
    elif instance.Product_type == 'D':
        obj = Tay_Nhuom.objects.get(BatchID=instance.Dye_ID)
    obj.save()

@receiver(post_delete, sender=Cang)
def post_save_Cang(sender, instance, **kwargs):
    if instance.Product_type == 'P':
        obj = Tay_In.objects.get(BatchID=instance.Print_ID)
    elif instance.Product_type == 'D':
        obj = Tay_Nhuom.objects.get(BatchID=instance.Dye_ID)
    obj.save()
