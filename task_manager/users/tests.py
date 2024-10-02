from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.users_list_url = reverse('user_list')
        self.login_url = reverse('login')
        self.form_data = {'username': 'bear',
                          'first_name': 'Nikita',
                          'last_name': 'Medvedev',
                          'password1': 'oldnew345',
                          'password2': 'oldnew345'}

    def test_user_list_view(self):
        self.client.login(username=self.user1.username, password='oldnew345')

        response = self.client.get(self.users_list_url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

        self.assertIn(self.user1, response.context['users'])
        self.assertIn(self.user2, response.context['users'])
