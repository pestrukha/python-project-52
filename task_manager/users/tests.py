from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user1.set_password('superpassword098')
        self.user1.save()
        self.user2.set_password('parol1357')
        self.user2.save()
        self.users_list_url = reverse('user_list')
        self.login_url = reverse('login')
        self.signup_url = reverse('user_create')
        self.user_update_url = reverse('user_update', args=[self.user1.pk])
        self.form_data = {'username': 'bear',
                          'first_name': 'Nikita',
                          'last_name': 'Medvedev',
                          'password1': 'oldnew345',
                          'password2': 'oldnew345'}

    def test_user_list_view(self):
        response = self.client.get(self.users_list_url)

        self.assertEqual(response.status_code, 200)

        users_in_context = response.context['users']
        self.assertIn(self.user1, users_in_context)
        self.assertIn(self.user2, users_in_context)

        self.assertEqual(len(users_in_context), 2)

    def test_create_user(self):
        response = self.client.post(self.signup_url, self.form_data)

        self.assertRedirects(response, self.login_url)

        new_user = get_user_model().objects.get(username='bear')
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.first_name, 'Nikita')
        self.assertEqual(new_user.last_name, 'Medvedev')

        login_successful = self.client.login(username='bear', password='oldnew345')
        self.assertTrue(login_successful)

    def test_update_user(self):
        self.client.force_login(self.user2)
        update_user = reverse('user_update', args=[2])

        get_response = self.client.get(update_user)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(update_user,
                                         self.form_data, follow=True)
        self.assertRedirects(post_response, self.users_list_url)
        updated_user = get_user_model().objects.get(pk=2)
        self.assertEqual(updated_user.username, 'bear')

    def test_user_cannot_update_other_user(self):
        self.client.force_login(self.user1)

        update_user_url = reverse('user_update', args=[self.user2.pk])
        response = self.client.post(update_user_url, self.form_data, follow=True)

        self.assertRedirects(response, self.users_list_url)

        updated_user2 = get_user_model().objects.get(pk=self.user2.pk)
        self.assertNotEqual(updated_user2.username, self.form_data['username'])
