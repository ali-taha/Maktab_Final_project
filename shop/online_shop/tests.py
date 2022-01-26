from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from model_mommy import mommy
from .models import Store, StoreType, ProductTag, Product, Basket, ProductCategory

User = get_user_model()


class TestAPI(APITestCase):
     def setUp(self):
        self.user = User.objects.create(
            username="test",
            password="123",
            phone_number='09122975260',
            email='test@gmail.com'
        )
        self.store_type= StoreType.objects.create(title="Type")
        self.store_type2= StoreType.objects.create(title="Type2")
        self.product_tag= ProductTag.objects.create(title="Tag1")
        self.product_tag2= ProductTag.objects.create(title="Tag2")
        self.product_category1= ProductCategory.objects.create(title="Category1", description="category1")

        self.store1 = Store.objects.create(owner=self.user, title='store1', type = self.store_type, status='con', description="test",)
        self.store2 = Store.objects.create(owner=self.user, title='store2', type = self.store_type2, status='rev', description="test",)

        self.product1 = Product.objects.create(store=self.store1, category=self.product_category1, title='product1', price = 1200,stock=10)
        self.product2 = Product.objects.create(store=self.store2, category=self.product_category1, title='product2', price = 2000,stock=0)

        self.basket1 = Basket.objects.create(owner=self.user, store=self.store1, status='rev')

 

     def test_user_sign_up(self):
        data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09037226589"}
        url = reverse("sign_up_api")
        resp = self.client.post(url, data=data)
        print(resp.data)
        self.assertEqual(resp.status_code, 201)

     def test_wrong_user_sign_up(self):
        url = reverse("sign_up_api")
        data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09037226589"}
        self.client.post(url, data=data)
        data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09037226589"}
        resp = self.client.post(url, data=data)
        print(resp.data)
        self.assertEqual(resp.status_code, 400)
        
     def test_user_sgn_in(self):
        data = {"username": "testi", "password": "testi", "email":"testi@gmail.com", "phone_number":"09037226589"}
        url = reverse("sign_up_api")
        resp = self.client.post(url, data=data)
        data = {"username": "testi", "password": "testi"}
        url2 = reverse("sign_in_api")
        resp2 = self.client.post(url2, data=data)
        self.assertEqual(resp2.status_code, 200)   

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
        self.assertEqual(len(resp.data), 1)

     def test_type_list(self):
        self.client.force_authenticate(self.user)
        url= reverse("store_type_list_api") 
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 2)

     def test_product_list(self):
        self.client.force_authenticate(self.user)
        url= reverse("product_list_api", args=(self.store1.pk,)) 
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)


     def test_create_basket(self):
        self.client.force_authenticate(self.user)
        url = reverse("basket_create_api", args=(self.product1.pk,))   
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data.get('basket_id'), '3')

     def test_add_basket_item(self):
        self.client.force_authenticate(self.user)
        data = {"count":1}
        url= reverse("basket_add_item_api", kwargs={"basket_id": f'{self.basket1}', "product_id": self.product1.id,}) 
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data.get('Basket Item Successfully added'), '1')

     def test_delete_basket_item(self):
        self.client.force_authenticate(self.user)
        data = {"count":1}
        url= reverse("basket_add_item_api", kwargs={"basket_id": f'{self.basket1}', "product_id": self.product1.id,}) 
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data.get('Basket Item Successfully added'), '3') 
        url= reverse("delete_basket_item_api", args=(1,))
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 404)


     def test_pay_basket_api(self):
         self.client.force_authenticate(self.user)
         basket1 = self.basket1
         url= reverse("pay_basket_api", args=(f'{self.basket1.pk}',))
         resp = self.client.put(url)
         print(resp.data)
         # self.basket1.status = "con"
         self.assertEqual(resp.status_code, 200)
         print(self.basket1.status)


     def test_show_baskets_api(self):
         self.client.force_authenticate(self.user)
         url= reverse("show_baskets_api",args=(f'rev',))
         resp=self.client.get(url) 
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(len(resp.data), 1)





    



 






 

    

