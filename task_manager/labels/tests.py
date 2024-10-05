from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label


class TestLabelsCase(TestCase):
    fixtures = ['labels.json', 'users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)
        self.labels_url = reverse('label_list')
        self.create_label_url = reverse('label_create')
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
