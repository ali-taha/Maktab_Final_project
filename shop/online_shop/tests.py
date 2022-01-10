from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from model_mommy import mommy
from .models import Store, StoreType, ProductTag, Product

User = get_user_model()


class TestAPI(APITestCase):
     def setUp(self):
        self.user = User.objects.create(
            username="test",
            password="123",
            phone_number='09122655658',
            email='test@gmail.com'
        )
        self.store_type= StoreType.objects.create(title="Type")
        self.store_type2= StoreType.objects.create(title="Type2")
        self.product_tag= ProductTag.objects.create(title="Tag1")
        self.product_tag2= ProductTag.objects.create(title="Tag2")

        mommy.make(Store, status='con',type=self.store_type, _quantity=2)
        self.store3 = mommy.make(Store, status='con',type=self.store_type2)
        mommy.make(Store, status='rev', type=self.store_type2, _quantity=2)
        mommy.make(Product, make_m2m=self.product_tag, stock=10, _quantity=2)
        mommy.make(Product, make_m2m=self.product_tag2, stock=0, _quantity=2)


     def test_user_sign_up(self):
        data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09122211"}
        url = reverse("sign_up_api")
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)

    #  def test_user_sgn_in(self):
    #     data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09122211"}
    #     url = reverse("sign_up_api")
    #     resp = self.client.post(url, data=data)
    #     data = {"username": "testi", "password": "testi"}
    #     url2 = reverse("sign_in_api")
    #     resp2 = self.client.post(url2, data=data)
    #     print(resp2.data)
    #     self.assertEqual(resp2.status_code, 201)   

     def test_user_profile(self):
         self.client.force_authenticate(self.user)
         url= reverse("profile_api", args=(self.user.username,))
         data = {"email":"new@gmail.com"}
         resp = self.client.put(url, data=data)
         self.assertEqual(resp.status_code, 200)

     def test_store_list(self):
        self.client.force_authenticate(self.user)
        url= reverse("store_list_api")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 3)

     def test_type_list(self):
        self.client.force_authenticate(self.user)
        url= reverse("store_type_list_api") 
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 2)

     
     def test_product_list(self):
        self.client.force_authenticate(self.user)
        url= reverse("product_list_api", args=(self.store3.id,)) 
        resp = self.client.get(url)
 

    

