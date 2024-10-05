from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class TestLabelsCase(TestCase):
    fixtures = ['labels.json', 'users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)
        self.labels_url = reverse('label_list')
        self.create_label_url = reverse('label_create')
        self.update_label_url = reverse('label_update', kwargs={'pk': 1})
        self.form_data = {'name': 'new label'}

    def test_label_list_view(self):
        response = self.client.get(self.labels_url)

        self.assertEqual(response.status_code, 200)

        labels_in_context = response.context['labels']

        self.assertTrue(Label.objects.filter(pk=1).exists())
        self.assertTrue(Label.objects.filter(pk=2).exists())

        self.assertIn(Label.objects.get(pk=1), labels_in_context)
        self.assertIn(Label.objects.get(pk=2), labels_in_context)

        self.assertEqual(len(labels_in_context), Label.objects.count())

    def test_create_label(self):
        response = self.client.post(self.create_label_url, self.form_data)

        self.assertRedirects(response, self.labels_url)

        new_label = Label.objects.get(name='new label')
        self.assertIsNotNone(new_label)

    def test_update_label(self):
        get_response = self.client.get(self.update_label_url)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.update_label_url, self.form_data, follow=True)

        self.assertRedirects(post_response, self.labels_url)

        updated_label = Label.objects.get(pk=1)
        self.assertEqual(updated_label.name, 'new label')

    def test_delete_used_label(self):
        self.label = Label.objects.create(name='тест')
        self.status = Status.objects.create(name='тестирование')

        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user,
            executor=self.user2
        )
        self.task.labels.add(self.label)

        delete_label_url = reverse('label_delete', args=[self.label.pk])
        response = self.client.post(delete_label_url, follow=True)

        self.assertRedirects(response, reverse('label_list'))

        label_still_exists = Label.objects.filter(pk=self.label.pk).exists()
        self.assertTrue(label_still_exists)

        task_still_exists = Task.objects.filter(pk=self.task.pk).exists()
        self.assertTrue(task_still_exists)

    def test_delete_unused_label(self):
        self.label = Label.objects.create(name='неиспользуемый лейбл')

        delete_label_url = reverse('label_delete', args=[self.label.pk])
        response = self.client.post(delete_label_url, follow=True)

        self.assertRedirects(response, reverse('label_list'))

        label_still_exists = Label.objects.filter(pk=self.label.pk).exists()
        self.assertFalse(label_still_exists)
