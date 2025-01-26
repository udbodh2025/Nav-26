from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db.models import Sum
from .models import MenuItem, Module, Form, Task, Project, Transaction
from .forms import TaskForm, ProjectForm, TransactionForm, TaskFormSet

# Existing views remain unchanged
@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def module_view(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.user.groups.filter(id__in=module.menu_item.groups.all()).exists() or not module.menu_item.groups.exists():
        forms = module.forms.all()
        tasks = module.tasks.all()
        return render(request, 'core/module.html', {'module': module, 'forms': forms, 'tasks': tasks})
    else:
        return redirect('home')

@login_required
def project_list(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    projects = module.projects.all()
    return render(request, 'core/project_list.html', {'module': module, 'projects': projects})

@login_required
def project_create(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        formset = TaskFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            project = form.save(commit=False)
            project.module = module
            project.save()
            formset.instance = project
            formset.save()
            messages.success(request, _('Project created successfully.'))
            return redirect('project_list', module_id=module.id)
    else:
        form = ProjectForm()
        formset = TaskFormSet()
    return render(request, 'core/project_form.html', {'form': form, 'formset': formset, 'module': module})


@login_required
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, _('Project updated successfully.'))
            return redirect('project_list', module_id=project.module.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form, 'project': project, 'module': project.module})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        module_id = project.module.id
        project.delete()
        messages.success(request, _('Project deleted successfully.'))
        return redirect('project_list', module_id=module_id)
    return render(request, 'core/project_confirm_delete.html', {'project': project})

@login_required
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        formset = TaskFormSet(request.POST, instance=project)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _('Project updated successfully.'))
            return redirect('project_list', module_id=project.module.id)
    else:
        form = ProjectForm(instance=project)
        formset = TaskFormSet(instance=project)
    return render(request, 'core/project_form.html', {'form': form, 'formset': formset, 'project': project, 'module': project.module})


@login_required
def transaction_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    transactions = project.transactions.all()
    
    income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income - expenses

    return render(request, 'core/transaction_list.html', {
        'project': project,
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance
    })

@login_required
def transaction_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.project = project
            transaction.created_by = request.user
            transaction.save()
            messages.success(request, _('Transaction created successfully.'))
            return redirect('transaction_list', project_id=project.id)
    else:
        form = TransactionForm(initial={'project': project})
    return render(request, 'core/transaction_form.html', {'form': form, 'project': project})

@login_required
def transaction_update(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, _('Transaction updated successfully.'))
            return redirect('transaction_list', project_id=transaction.project.id)
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'core/transaction_form.html', {'form': form, 'transaction': transaction, 'project': transaction.project})

@login_required
def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        project_id = transaction.project.id
        transaction.delete()
        messages.success(request, _('Transaction deleted successfully.'))
        return redirect('transaction_list', project_id=project_id)
    return render(request, 'core/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def all_applications(request):
    user_groups = request.user.groups.all()
    applications = MenuItem.objects.filter(is_application=True).filter(groups__in=user_groups).distinct()
    return render(request, 'core/all_applications.html', {'applications': applications})

@login_required
def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, 'core/task_list.html', {'project': project, 'tasks': tasks})

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            messages.success(request, _('Task created successfully.'))
            return redirect('task_list', project_id=project.id)
    else:
        form = TaskForm(initial={'project': project})
    return render(request, 'core/task_form.html', {'form': form, 'project': project})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task updated successfully.'))
            return redirect('task_list', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form, 'task': task, 'project': task.project})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        project_id = task.project.id
        task.delete()
        messages.success(request, _('Task deleted successfully.'))
        return redirect('task_list', project_id=project_id)
    return render(request, 'core/task_confirm_delete.html', {'task': task})