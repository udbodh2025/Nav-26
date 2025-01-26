from django import forms
from django.forms import inlineformset_factory
from .models import Task, Project, Transaction

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'description', 'date', 'project']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


TaskFormSet = inlineformset_factory(
    Project,
    Task,
    fields=['title', 'description', 'status', 'assigned_to'],
    extra=1,
    can_delete=True
)

