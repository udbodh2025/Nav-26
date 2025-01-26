from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from core import views

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('all-applications/', views.all_applications, name='all_applications'),
    path('module/<int:module_id>/', views.module_view, name='module'),
    path('module/<int:module_id>/projects/', views.project_list, name='project_list'),
    path('module/<int:module_id>/projects/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/update/', views.project_update, name='project_update'),
    path('project/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:project_id>/tasks/', views.task_list, name='task_list'),
    path('project/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/update/', views.task_update, name='task_update'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('project/<int:project_id>/transactions/', views.transaction_list, name='transaction_list'),
    path('project/<int:project_id>/transactions/create/', views.transaction_create, name='transaction_create'),
    path('transaction/<int:transaction_id>/update/', views.transaction_update, name='transaction_update'),
    path('transaction/<int:transaction_id>/delete/', views.transaction_delete, name='transaction_delete'),
    path('i18n/', include('django.conf.urls.i18n')),
)
