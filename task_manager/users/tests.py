from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class UserTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user1.set_password('superpassword098')
        self.user1.save()
        self.user2.set_password('parol1357')
        self.user2.save()
        self.client.force_login(self.user1)
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

    def test_update_other_user(self):
        self.client.force_login(self.user1)

        update_user_url = reverse('user_update', args=[self.user2.pk])
        response = self.client.post(update_user_url, self.form_data, follow=True)

        self.assertRedirects(response, self.users_list_url)

        updated_user2 = get_user_model().objects.get(pk=self.user2.pk)
        self.assertNotEqual(updated_user2.username, self.form_data['username'])

    def test_delete_other_user(self):
        self.client.force_login(self.user1)

        delete_user_url = reverse('user_delete', args=[self.user2.pk])
        response = self.client.post(delete_user_url, follow=True)

        self.assertRedirects(response, self.users_list_url)

        user_still_exists = get_user_model().objects.filter(pk=self.user2.pk).exists()
        self.assertTrue(user_still_exists)

    def test_delete_user_with_tasks(self):
        self.status = Status.objects.create(
            name="Новый",
        )

        self.task = Task.objects.create(
            name='Тест',
            description='Описание',
            status=self.status,
            author=self.user2,
            executor=self.user1
        )

        self.client.force_login(self.user1)
        delete_user_url = reverse('user_delete', args=[self.user2.pk])
        response = self.client.post(delete_user_url, follow=True)

        self.assertRedirects(response, reverse('user_list'))

        user_still_exists = get_user_model().objects.filter(pk=self.user2.pk).exists()
        self.assertTrue(user_still_exists)

        task_still_exists = Task.objects.filter(pk=self.task.pk).exists()
        self.assertTrue(task_still_exists)

    def test_delete_user_without_tasks(self):
        self.client.force_login(self.user1)
        delete_user_url = reverse('user_delete', args=[self.user1.pk])

        response = self.client.post(delete_user_url, follow=True)

        self.assertRedirects(response, reverse('user_list'))

        user_still_exists = get_user_model().objects.filter(pk=self.user1.pk).exists()
        self.assertFalse(user_still_exists)
