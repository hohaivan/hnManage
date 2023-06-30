from datetime import datetime

from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver
from .models import YarnPay, Delivery, YarnTransfer, Warehouse, Warehouse2, YarnDebt_LY, YarnOrder
from ledger.models import ledger, Transactions


@receiver(post_save, sender=YarnPay)
def post_save_create_update_YarnPay(sender, instance, created, **kwargs):
    # define changable variables:
    Transaction_id = 2
    
    if created:
        obj = ledger.objects.create(Date=instance.Date, Amount=instance.Pay, Transaction_id=Transaction_id,
                                    Description=instance.Vendor.Name, Creator=instance.Creator,
                                    Database='YarnPay', Address=instance.id)
        obj.save(Sync=True, Signal=True)

    else:
        try:
            obj = ledger.objects.get(Database='YarnPay', Address=instance.id)
            obj.Date = instance.Date
            obj.Amount = instance.Pay
            obj.Transaction_id = Transaction_id
            obj.Description = instance.Vendor.Name
            obj.Creator = instance.Creator
            obj.Database = 'YarnPay'
            obj.Address = instance.id
            obj.save(Sync=True, Signal=True)
        except:
            if instance.Sync:
                obj = ledger.objects.create(Date=instance.Date, Amount=instance.Pay, Transaction_id=Transaction_id,
                                            Description=instance.Vendor.Name, Creator=instance.Creator,
                                            Database='YarnPay', Address=instance.id)
                obj.save(Sync=True, Signal=True)


@receiver(pre_delete, sender=YarnPay)
def pre_delete_YarnPay(sender, instance, **kwargs):
    try:
        obj = ledger.objects.get(Database='YarnPay', Address=instance.id)
        obj.delete(Signal=True)
    except:
        pass


@receiver(pre_delete, sender=ledger)
def pre_delete_ledger(sender, instance, **kwargs):
    if instance.Database == 'YarnPay':
        obj = YarnPay.objects.get(id=instance.Address)
        obj.save(Sync=False)


@receiver(post_save, sender=Warehouse)
def post_save_Warehouse(sender, instance, created, **kwargs):
    try:
        check = Warehouse2.objects.get(Name_id=instance.id)
        return None
    except:
        obj = Warehouse2.objects.create(Name_id=instance.id)
        obj.save()


@receiver(post_save, sender=Delivery)
def post_save_Delivery(sender, instance, created, **kwargs):
    if created:
        obj = YarnTransfer.objects.create(Date=instance.Date, YarnType=instance.OrderID.YarnType,
                                          YarnStats=instance.OrderID.YarnStats, YarnCode=instance.YarnCode,
                                          Origin=None, Destination=instance.Warehouse, Box_Pack=instance.OrderID.Box_Pack,
                                          BoxQty=instance.BoxQty, Weight=instance.Weight, Note='NCC: '+str(instance.OrderID.Vendor),
                                          Creator=instance.Creator, Database='Delivery', Address=instance.id)
        obj.save(Sync=True, Signal=True)
    else:
        try:
            obj = YarnTransfer.objects.get(Database='Delivery', Address=instance.id)
            obj.Date = instance.Date
            obj.YarnType = instance.OrderID.YarnType
            obj.YarnCode = instance.YarnCode
            obj.Origin = None
            obj.Destination = instance.Warehouse
            obj.Box_Pack = instance.OrderID.Box_Pack
            obj.BoxQty = instance.BoxQty
            obj.Weight = instance.Weight
            obj.Note = 'NCC: '+str(instance.OrderID.Vendor)
            obj.Creator = instance.Creator
            obj.Database = 'Delivery'
            obj.Address = instance.id
            obj.save(Sync=True, Signal=True)
        except:
            if instance.Sync:
                obj = YarnTransfer.objects.create(Date=instance.Date, YarnType=instance.OrderID.YarnType,
                                                  YarnStats=instance.OrderID.YarnStats, YarnCode=instance.YarnCode,
                                                  Origin=None, Destination=instance.Warehouse,
                                                  Box_Pack=instance.OrderID.Box_Pack,
                                                  BoxQty=instance.BoxQty, Weight=instance.Weight,
                                                  Note='NCC: ' + str(instance.OrderID.Vendor),
                                                  Creator=instance.Creator, Database='Delivery', Address=instance.id)
                obj.save(Sync=True, Signal=True)


@receiver(pre_delete, sender=Delivery)
def pre_delete_Delivery(sender, instance, **kwargs):
    try:
        obj = YarnTransfer.objects.get(Database='Delivery', Address=instance.id)
        obj.delete(Signal=True)
    except:
        pass


@receiver(pre_delete, sender=YarnTransfer)
def pre_delete_YarnTransfer(sender, instance, **kwargs):
    if instance.Database == 'Delivery':
        obj = Delivery.objects.get(id=instance.Address)
        obj.save(Sync=False)


@receiver(post_save, sender=YarnDebt_LY)
def post_save_Yarn_Debt(sender, instance, created, **kwargs):
    # calculate amount in year
    Delivered = Delivery.objects.filter(OrderID__Vendor=instance.Vendor, year=instance.Year+1)
    Pay = YarnPay.objects.filter(Vendor=instance.Vendor, year=instance.Year + 1)
    Buy_value = sum(row.PayValue for row in Delivered)
    Pay_value = sum(row.Pay for row in Pay)
    Debt_that_year = Buy_value - Pay_value
    # end calculation

    if created:
        if instance.Year < datetime.now().year:
            if not YarnDebt_LY.objects.filter(Vendor=instance.Vendor, Year=instance.Year+1).exists():
                obj = YarnDebt_LY.objects.create(Vendor=instance.Vendor, Year=instance.Year+1, Debt=instance.Debt+Debt_that_year)
                obj.save()

@receiver(pre_save, sender=YarnPay)
def pre_save_YarnPay(sender, instance, **kwargs):
    try:
        instance._old_instance = YarnPay.objects.get(pk=instance.pk)
    except YarnPay.DoesNotExist:
        instance._old_instance = None

@receiver(post_save, sender=YarnPay)
def post_save_YarnPay(sender, instance, created, **kwargs):
    obj = YarnDebt_LY.objects.filter(Vendor=instance.Vendor, Year=instance.year)
    if obj.exists():
        target = obj.get()
    else:
        target = YarnDebt_LY.objects.create(Vendor=instance.Vendor, Year=instance.year, Debt=0)
    target.Debt = target.Auto_Calculation
    target.save()
    if not created:
        old_instance = instance._old_instance
        old_obj = YarnDebt_LY.objects.filter(Vendor=old_instance.Vendor, Year=old_instance.year)
        if old_obj.exists():
            old_target = old_obj.get()
        else:
            old_target = YarnDebt_LY.objects.create(Vendor=old_instance.Vendor, Year=old_instance.year, Debt=0)
        old_target.Debt = old_target.Auto_Calculation
        old_target.save()

@receiver(post_save, sender=Delivery)
def post_save_Delivery_adjust_YarnOrder_YarnDebt(sender, instance, created, **kwargs):
    obj = YarnDebt_LY.objects.filter(Vendor=instance.OrderID.Vendor, Year=instance.year)
    if obj.exists():
        target = YarnDebt_LY.objects.get(Vendor=instance.OrderID.Vendor, Year=instance.year)
    else:
        target = YarnDebt_LY.objects.create(Vendor=instance.OrderID.Vendor, Year=instance.year, Debt=0)
    target.Debt = target.Auto_Calculation
    target.save()

    obj2 = YarnOrder.objects.get(BatchID=instance.OrderID)
    obj2.save()

@receiver(post_delete, sender=Delivery)
def post_delete_Delivery(sender, instance, **kwargs):
    obj = YarnOrder.objects.get(BatchID=instance.OrderID)
    obj.save()

@receiver(post_delete, sender=YarnPay)
def post_delete_YarnPay(sender, instance, **kwargs):
    obj = YarnDebt_LY.objects.filter(Vendor=instance.Vendor, Year=instance.year)
    if obj.exists():
        target = YarnDebt_LY.objects.get(Vendor=instance.Vendor, Year=instance.year)
    else:
        target = YarnDebt_LY.objects.create(Vendor=instance.Vendor, Year=instance.year, Debt=0)
    target.Debt = target.Auto_Calculation
    target.save()

@receiver(post_delete, sender=Delivery)
def post_delete_Delivery(sender, instance, **kwargs):
    obj = YarnDebt_LY.objects.filter(Vendor=instance.OrderID.Vendor, Year=instance.year)
    if obj.exists():
        target = YarnDebt_LY.objects.get(Vendor=instance.OrderID.Vendor, Year=instance.year)
    else:
        target = YarnDebt_LY.objects.create(Vendor=instance.OrderID.Vendor, Year=instance.year, Debt=0)
    target.Debt = target.Auto_Calculation
    target.save()
