from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task


class TaskTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json',
                'statuses.json', 'labels.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)
        self.tasks_url = reverse('task_list')
        self.task_create_url = reverse('task_create')
        self.task_update_url = reverse('task_update', args=[1])
        self.task_delete_url = reverse('task_delete', args=[1])
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.form_data = {'name': 'test task',
                          'status': 1,
                          'description': 'test description',
                          'executor': 1,
                          'labels': 1}

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

    def test_create_task(self):
        response = self.client.post(self.task_create_url, data=self.form_data)

        self.assertRedirects(response, self.tasks_url)

        self.assertTrue(Task.objects.filter(name='test task').exists())

        task = Task.objects.get(name='test task')
        self.assertEqual(task.description, 'test description')
        self.assertEqual(task.status.id, 1)
        self.assertEqual(task.executor.id, 1)

        self.assertEqual(task.labels.count(), 1)
        self.assertEqual(task.labels.first().id, 1)

    def test_update_task(self):
        updated_data = {
            'name': 'updated task',
            'status': 2,
            'description': 'updated description',
            'executor': 2,
            'labels': 2
        }

        response = self.client.post(self.task_update_url, data=updated_data)

        self.assertRedirects(response, self.tasks_url)

        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'updated task')
        self.assertEqual(self.task1.description, 'updated description')
        self.assertEqual(self.task1.status.id, 2)
        self.assertEqual(self.task1.executor.id, 2)
        self.assertEqual(self.task1.labels.count(), 1)
        self.assertEqual(self.task1.labels.first().id, 2)

    def test_delete_task(self):
        response = self.client.post(self.task_delete_url)

        self.assertRedirects(response, self.tasks_url)

        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_filter_tasks(self):
        response = self.client.get(f'{self.tasks_url}?status=1&executor=1&label=')
        tasks_list = response.context['tasks']

        self.assertEqual(len(tasks_list), 1)
        task = tasks_list[0]
        self.assertEqual(task.name, 'Питон')
        self.assertEqual(task.executor.id, 1)
        self.assertEqual(task.status.id, 1)

    def test_one_task(self):
        self.one_task_url = reverse('one_task', args=[1])

        response = self.client.get(self.one_task_url)
        self.assertEqual(response.status_code, 200)

        task = response.context['task']
        self.assertEqual(task.name, self.task1.name)
        self.assertEqual(task.description, self.task1.description)
        self.assertEqual(task.author.id, self.task1.author.id)
        self.assertEqual(task.executor.id, self.task1.executor.id)
        self.assertEqual(task.status.id, self.task1.status.id)
        self.assertEqual(task.created_at, self.task1.created_at)
