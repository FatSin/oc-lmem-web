import requests
import json

from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Substitute
from .findsubstitute import findsubstitute

#sys.path.append(sys.path[0] + "/..")



# Create your tests here.

class Routetesting(TestCase):
    """Test the views of 'searchapp' app."""
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    def test_results_page(self):
        response = self.client.get(reverse('results'))
        self.assertEqual(response.status_code, 200)
    def test_product_page(self):
        response = self.client.get(reverse('product'))
        self.assertEqual(response.status_code, 200)
    def test_myproducts_page(self):
        response = self.client.get(reverse('myproducts'))
        self.assertEqual(response.status_code, 200) 
    def test_account_page(self):
        response = self.client.get(reverse('myaccount'))
        self.assertEqual(response.status_code, 200)

        
class APItesting(TestCase):
    def test_off_api(self):
        response = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms=coca&countries=en:france&search_simple=1&action=process&json=1")
        self.assertEqual(response.status_code, 200)
    
    
class TestFindSubstitute(TestCase):

    def setUp(self):
        self.data = {
                        "count":1,
                        "products":
                            [{
                            "product_name":"Comté AOP (34% MG)",
                            "nutrition_grades":"d",
                            "url":"https://world.openfoodfacts.org/product/3123930650064/comte-aop-34-mg-entremont",
                            "categories":"Frais,Produits laitiers,Produits labellisés,Fromages,Fromages à pâte pressée cuite,Fromages de vache,Fromages de France,Produits AOC,Fromages au lait cru,Fromages labéllisés,Fromages AOC,Comté",
                            "image_url":"https://static.openfoodfacts.org/images/products/312/393/065/0064/front_fr.77.400.jpg"
                            }],
                        "page_size":"1",
                        "skip":0,
                        "page":1
                        }
                        
        #self.data = json.dumps(text)
        self.product = [self.data["products"][0]["product_name"], self.data["products"][0]["categories"].split(','), self.data["products"][0]["nutrition_grades"], self.data["products"][0]["image_url"],self.data["products"][0]["url"]]

        Category.objects.create(CategoryName="Fromages", id=1)
        Product.objects.create(ProductName="Test-comte", Grade="a",
                                       CatNum=1, ImageLink="toto",Link="toto")
        self.sub = Product.objects.get(ProductName="Test-comte")
        

    def test_find_substitute(self):

        results = findsubstitute(self.product)
        
        assert results[0][0].ProductName == "Test-comte"
        assert results[1] == Product.objects.get(ProductName="Comté AOP (34% MG)").id
        assert results[2] == self.sub.id
        assert results[3] == self.sub.ImageLink
        assert results[4] == self.sub.Grade.upper()
        

        
class DealwithProduct(TestCase):
    
    def setUp(self):
        Product.objects.create(ProductName="Test-product", Grade="a",
                                       CatNum=1, ImageLink="toto",Link="toto")
        self.product = Product.objects.get(ProductName="Test-product")
        self.prodid = self.product.id

    def test_product_search(self):
        response = self.client.get(reverse('product'),args=(self.prodid,))
        self.assertEqual(response.status_code, 200)

        
class DealwithUser(TestCase):

    #def SetUp(self):
    #    self.usern = 'username'
    #    self.passw = 'password'
    
    
    def test_myproducts_page(self):
        response = self.client.get(reverse('myproducts'))
        self.assertEqual(response.status_code, 200) 
    def test_account_page(self):
        response = self.client.get(reverse('index'),args=('username','self.passw',))
        self.assertEqual(response.status_code, 200)