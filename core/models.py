from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

# Existing models (MenuItem, Module, Form, Project, Task, Transaction) remain unchanged
class MenuItem(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    url = models.CharField(_('URL'), max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(_('Order'), default=0)
    groups = models.ManyToManyField(Group, blank=True, related_name='menu_items')
    is_application = models.BooleanField(_('Is Application'), default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Module(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='modules')
    users = models.ManyToManyField(User, related_name='modules')

    def __str__(self):
        return self.name

class Form(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='forms')
    content = models.TextField(_('Content'))

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Task(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(_('Status'), max_length=20, choices=[
        ('todo', _('To Do')),
        ('in_progress', _('In Progress')),
        ('done', _('Done'))
    ], default='todo')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', _('Income')),
        ('expense', _('Expense')),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    transaction_type = models.CharField(_('Type'), max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(_('Description'), max_length=255)
    date = models.DateField(_('Date'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount}"

    class Meta:
        ordering = ['-date', '-created_at']

class Unit(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class Level(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']

class Bank(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    swift_code = models.CharField(_('SWIFT Code'), max_length=11, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Currency(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=3, unique=True)
    symbol = models.CharField(_('Symbol'), max_length=5)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name_plural = 'Currencies'
        ordering = ['name']

class Designation(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class StaffDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_details')
    employee_id = models.CharField(_('Employee ID'), max_length=20, unique=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, related_name='staff')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, related_name='staff')
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, related_name='staff')
    date_of_birth = models.DateField(_('Date of Birth'))
    date_of_joining = models.DateField(_('Date of Joining'))
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, related_name='staff')
    bank_account_number = models.CharField(_('Bank Account Number'), max_length=50)
    preferred_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='staff')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    class Meta:
        verbose_name = 'Staff Detail'
        verbose_name_plural = 'Staff Details'
        ordering = ['user__last_name', 'user__first_name']

