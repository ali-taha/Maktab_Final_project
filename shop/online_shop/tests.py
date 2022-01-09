from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from model_mommy import mommy

User = get_user_model()


class TestAPI(APITestCase):
     def setUp(self):
        self.user = User.objects.create(
            username="test",
            password="123",
        )

     def test_user_sign_up(self):
        data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09122211"}
        url = reverse("sign_up_api")
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)

     def test_user_sgn_in(self):
        data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09122211"}
        url = reverse("sign_up_api")
        resp = self.client.post(url, data=data)
        data = {"username": "testi", "password": "testi"}
        url2 = reverse("sign_in_api")
        resp2 = self.client.post(url2, data=data)
        self.assertEqual(resp.status_code, 201)   
