from django.test import TestCase
from django.contrib.auth.models import User
from .models import Todo
from random import choice
from string import ascii_letters, digits
from django.utils import timezone


# Create your tests here.
class UserTestCase(TestCase):
    setup_users = {'TestUser': 'TestPassword', 'Smokevich': 'randompassword!'}

    def setUp(self) -> None:
        for name, password in self.setup_users.items():
            User.objects.create(
                username=name, 
                password=password)
            

    def test_validate_data(self) -> None:
        "Validate User Model"
        for name, password in self.setup_users.items():
            user = User.objects.filter(username=name, password=password).get()
            self.assertEqual(user.username, name, msg='Name invalid after add in DB.')
            self.assertEqual(user.password, password, msg='Password invalid after add in DB.')

    def test_add_user(self):
        "Add more users"
        symbols = ascii_letters + digits
        for _ in range(100):
            name = ''.join([choice(symbols) for _ in range(16)])
            password = ''.join([choice(symbols) for _ in range(16)])
            User.objects.create_user(username=name, password=password)
        
        users = User.objects.all()
        self.assertGreater(len(users), 100, msg='100 users not added.')


        
class TaskTestCase(TestCase):
    setup_task = {}
    def setUp(self) -> None:
        User.objects.create_user('User', password='1111155555')
        user = User.objects.filter(username='User').get()

        Todo.objects.create(
            name='NameTask',
            description='DescriptionTask',
            important=True,
            user_id=user)
        
        
    def test_validate_data(self) -> None:
        "Validate Task Model"
        task = Todo.objects.first()
        self.assertEqual(task.name, 'NameTask', msg='Task name invalid')
        self.assertEqual(task.description, 'DescriptionTask', msg='Task description invalid')
        self.assertTrue(task.important, msg='Task important invalid')
        

    def test_update_data(self) -> None:
        "Update data in DB"
        Todo.objects.filter(id=1).update(description='AnotherTask', important=False)
        task = Todo.objects.filter(id=1).get()
        self.assertEqual(task.description, 'AnotherTask', msg='Task description invalid after update')
        self.assertFalse(task.important, msg='Task important invalid after update')

    def test_complete_task(self):
        "Check complete task"
        task = Todo.objects.filter(id=1).get()
        task.endtime = timezone.now()
        task.save()
        self.assertIsNotNone(task.endtime, msg='Task not compleated')