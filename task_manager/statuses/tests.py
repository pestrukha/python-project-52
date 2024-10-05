from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status


class StatusTestCase(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)
        self.statuses_url = reverse('status_list')
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
