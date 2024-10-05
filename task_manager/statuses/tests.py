from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusTestCase(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user1)
        self.statuses_url = reverse('status_list')
        self.create_status_url = reverse('status_create')
        self.update_status_url = reverse('status_update', args=[1])
        self.form_data = {'name': 'new status'}

    def test_status_list_view(self):
        response = self.client.get(self.statuses_url)

        self.assertEqual(response.status_code, 200)

        statuses_in_context = response.context['statuses']

        self.assertTrue(Status.objects.filter(pk=1).exists())
        self.assertTrue(Status.objects.filter(pk=2).exists())

        self.assertIn(Status.objects.get(pk=1), statuses_in_context)
        self.assertIn(Status.objects.get(pk=2), statuses_in_context)

        self.assertEqual(len(statuses_in_context), Status.objects.count())

    def test_create_status(self):
        response = self.client.post(self.create_status_url, self.form_data)

        self.assertRedirects(response, self.statuses_url)

        new_status = Status.objects.get(name='new status')
        self.assertIsNotNone(new_status)

    def test_update_status(self):
        get_response = self.client.get(self.update_status_url)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.update_status_url, self.form_data, follow=True)
        self.assertRedirects(post_response, self.statuses_url)

        updated_status = Status.objects.get(pk=1)
        self.assertEqual(updated_status.name, 'new status')

    def test_delete_used_status(self):
        self.status = Status.objects.create(name='тестирование')

        # Создаём задачу с этим статусом
        self.task = Task.objects.create(
            name='Тест',
            description='Описание',
            status=self.status,
            author=self.user2,
            executor=self.user1
        )

        delete_status_url = reverse('status_delete', args=[self.status.pk])
        response = self.client.post(delete_status_url, follow=True)

        self.assertRedirects(response, reverse('status_list'))

        status_still_exists = Status.objects.filter(pk=self.status.pk).exists()
        self.assertTrue(status_still_exists)

        task_still_exists = Task.objects.filter(pk=self.task.pk).exists()
        self.assertTrue(task_still_exists)

    def test_delete_unused_status(self):
        self.status = Status.objects.create(name='выполнен')

        delete_status_url = reverse('status_delete', args=[self.status.pk])
        response = self.client.post(delete_status_url, follow=True)

        self.assertRedirects(response, reverse('status_list'))

        status_still_exists = Status.objects.filter(pk=self.status.pk).exists()
        self.assertFalse(status_still_exists)
