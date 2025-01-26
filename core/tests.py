from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import MenuItem, Module, Form
from django.urls import reverse

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.menu_item = MenuItem.objects.create(name='Test Menu', url='/test/')
        self.module = Module.objects.create(name='Test Module', menu_item=self.menu_item)
        self.module.users.add(self.user)
        self.form = Form.objects.create(name='Test Form', module=self.module, content='<p>Test content</p>')

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, 'Test Menu')
        self.assertEqual(self.menu_item.url, '/test/')

    def test_module_creation(self):
        self.assertEqual(self.module.name, 'Test Module')
        self.assertEqual(self.module.menu_item, self.menu_item)
        self.assertIn(self.user, self.module.users.all())

    def test_form_creation(self):
        self.assertEqual(self.form.name, 'Test Form')
        self.assertEqual(self.form.module, self.module)
        self.assertEqual(self.form.content, '<p>Test content</p>')

class ViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.menu_item = MenuItem.objects.create(name='Test Menu', url='/test/')
        self.module = Module.objects.create(name='Test Module', menu_item=self.menu_item)
        self.module.users.add(self.user)

    def test_home_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_module_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/module/{self.module.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/module.html')

    def test_menu_item_with_group(self):
        group = Group.objects.create(name='Test Group')
        self.user.groups.add(group)
        menu_item = MenuItem.objects.create(name='Group Menu', url='/group-test/')
        menu_item.groups.add(group)
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/')
        self.assertContains(response, 'Group Menu')

    def test_menu_item_without_group(self):
        group = Group.objects.create(name='Test Group')
        menu_item = MenuItem.objects.create(name='No Group Menu', url='/no-group-test/')
        menu_item.groups.add(group)
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/')
        self.assertNotContains(response, 'No Group Menu')

    def test_module_access_with_permission(self):
        group = Group.objects.create(name='Test Group')
        self.user.groups.add(group)
        menu_item = MenuItem.objects.create(name='Group Menu', url='/group-test/')
        menu_item.groups.add(group)
        module = Module.objects.create(name='Test Module', menu_item=menu_item)
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('module', args=[module.id]))
        self.assertEqual(response.status_code, 200)

    def test_module_access_without_permission(self):
        group = Group.objects.create(name='Test Group')
        menu_item = MenuItem.objects.create(name='No Group Menu', url='/no-group-test/')
        menu_item.groups.add(group)
        module = Module.objects.create(name='Test Module', menu_item=menu_item)
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('module', args=[module.id]))
        self.assertRedirects(response, reverse('home'))

