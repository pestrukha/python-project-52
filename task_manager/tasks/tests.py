from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task


class TaskTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json',
                'statuses.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)
        self.tasks_url = reverse('task_list')
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.form_data = {'name': 'test task',
                          'status': 1,
                          'description': 'test description',
                          'executor': 1,
                          'label': [2]}

    def test_task_list_view(self):
        response = self.client.get(self.tasks_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'tasks/task_list.html')

        tasks = response.context['tasks']
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertIn(self.task3, tasks)

        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)
