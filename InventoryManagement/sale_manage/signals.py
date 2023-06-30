from datetime import datetime

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Sales, Returned, Customer_Pay, Customer_Debt
from ledger.models import ledger, Transactions


@receiver(post_save, sender=Customer_Pay)
def post_save_create_update_CustomerPay(sender, instance, created, **kwargs):
    # define changable variables:
    Transaction_id = 1

    if created:
        obj = ledger.objects.create(Date=instance.Date, Amount=instance.Amount, Transaction_id=Transaction_id,
                                    Description=instance.Customer.name, Creator=instance.Creator,
                                    Database='Customer_Pay', Address=instance.id)
        obj.save(Sync=True, Signal=True)

    else:
        try:
            obj = ledger.objects.get(Database='Customer_Pay', Address=instance.id)
            obj.Date = instance.Date
            obj.Amount = instance.Amount
            obj.Transaction_id = Transaction_id
            obj.Description = instance.Customer.name
            obj.Creator = instance.Creator
            obj.Database = 'Customer_Pay'
            obj.Address = instance.id
            obj.save(Sync=True, Signal=True)
        except:
            if instance.Sync:
                obj = ledger.objects.create(Date=instance.Date, Amount=instance.Amount, Transaction_id=Transaction_id,
                                            Description=instance.Customer.name, Creator=instance.Creator,
                                            Database='Customer_Pay', Address=instance.id)
                obj.save(Sync=True, Signal=True)

@receiver(pre_delete, sender=Customer_Pay)
def pre_delete_CustomerPay(sender, instance, **kwargs):
    try:
        obj = ledger.objects.get(Database='Customer_Pay', Address=instance.id)
        obj.delete(Signal=True)
    except:
        pass

@receiver(pre_delete, sender=ledger)
def pre_delete_ledger(sender, instance, **kwargs):
    if instance.Database == 'Customer_Pay':
        obj = Customer_Pay.objects.get(id=instance.Address)
        obj.save(Sync=False)

# Update Customer Debt

@receiver(post_save, sender=Customer_Debt)
def post_save_Customer_Debt(sender, instance, created, **kwargs):
    # calculate amount in year
    Buy = Sales.objects.filter(Customer=instance.Customer, year=instance.Year+1)
    Back = Returned.objects.filter(Customer=instance.Customer, year=instance.Year + 1)
    Pay = Customer_Pay.objects.filter(Customer=instance.Customer, year=instance.Year + 1)
    Buy_value = sum(row.Amount for row in Buy)
    Back_value = sum(row.Amount for row in Back)
    Pay_value = sum(row.Amount for row in Pay)
    Amount_that_year = Buy_value - Back_value - Pay_value
    # end calculation

    if created:
        if instance.Year < datetime.now().year:
            if not Customer_Debt.objects.filter(Customer=instance.Customer, Year=instance.Year+1).exists():
                obj = Customer_Debt.objects.create(Customer=instance.Customer, Year=instance.Year+1, Amount=instance.Amount+Amount_that_year)
                obj.save()

@receiver(post_save, sender=Sales)
def post_save_Sales(sender, instance, created, **kwargs):
    obj = Customer_Debt.objects.filter(Customer=instance.Customer, Year=instance.year)
    if obj.exists():
        target = Customer_Debt.objects.get(Customer=instance.Customer, Year=instance.year)
    else:
        target = Customer_Debt.objects.create(Customer=instance.Customer, Year=instance.year, Amount=0)
    target.Amount = target.Auto_Calculation
    target.save()

@receiver(post_save, sender=Returned)
def post_save_Returned(sender, instance, created, **kwargs):
    obj = Customer_Debt.objects.filter(Customer=instance.Customer, Year=instance.year)
    if obj.exists():
        target = Customer_Debt.objects.get(Customer=instance.Customer, Year=instance.year)
    else:
        target = Customer_Debt.objects.create(Customer=instance.Customer, Year=instance.year, Amount=0)
    target.Amount = target.Auto_Calculation
    target.save()

@receiver(post_save, sender=Customer_Pay)
def post_save_Customer_Pay(sender, instance, created, **kwargs):
    obj = Customer_Debt.objects.filter(Customer=instance.Customer, Year=instance.year)
    if obj.exists():
        target = Customer_Debt.objects.get(Customer=instance.Customer, Year=instance.year)
    else:
        target = Customer_Debt.objects.create(Customer=instance.Customer, Year=instance.year, Amount=0)
    target.Amount = target.Auto_Calculation
    target.save()

@receiver(post_delete, sender=Sales)
def post_del_Sales(sender, instance, **kwargs):
    obj = Customer_Debt.objects.filter(Customer=instance.Customer, Year=instance.year)
    if obj.exists():
        target = Customer_Debt.objects.get(Customer=instance.Customer, Year=instance.year)
    else:
        target = Customer_Debt.objects.create(Customer=instance.Customer, Year=instance.year, Amount=0)
    target.Amount = target.Auto_Calculation
    target.save()

@receiver(post_delete, sender=Returned)
def post_del_Returned(sender, instance, **kwargs):
    obj = Customer_Debt.objects.filter(Customer=instance.Customer, Year=instance.year)
    if obj.exists():
        target = Customer_Debt.objects.get(Customer=instance.Customer, Year=instance.year)
    else:
        target = Customer_Debt.objects.create(Customer=instance.Customer, Year=instance.year, Amount=0)
    target.Amount = target.Auto_Calculation
    target.save()

@receiver(post_delete, sender=Customer_Pay)
def post_del_Customer_Pay(sender, instance, **kwargs):
    obj = Customer_Debt.objects.filter(Customer=instance.Customer, Year=instance.year)
    if obj.exists():
        target = Customer_Debt.objects.get(Customer=instance.Customer, Year=instance.year)
    else:
        target = Customer_Debt.objects.create(Customer=instance.Customer, Year=instance.year, Amount=0)
    target.Amount = target.Auto_Calculation
    target.save()