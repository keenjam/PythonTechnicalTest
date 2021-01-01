from rest_framework.test import APISimpleTestCase, APIClient
from django.test import TestCase
from .models import Bond
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200

class BondTesting(TestCase):
    def setUp(self):
        User.objects.create_user(username='origin', email='test@origin.com', password='iloveorigin')
        User.objects.create_user(username='adversary', email='test@adversay.com', password='password12345')
        self.createTokens()

    def test_unauthenticated_client(self):
        print("\n/////////////////////////////")
        print("TESTING UNAUTHENTICATED CLIENT")
        print("/////////////////////////////\n")
        resp = self.client.get("/bonds/")
        assert resp.status_code == 401

    def test_access_rights(self):
        print("\n/////////////////////")
        print("TESTING ACCESS RIGHTS")
        print("/////////////////////\n")
        token1 = Token.objects.get(user__username='origin')
        client1 = APIClient()
        client1.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)

        createData = {'isin':'GB0000121104', 'size':50000, 'currency':'USD', 'maturity':'2025-03-01', 'lei':'R0MUWSFPU8MPRO8K5P83'}
        resp = client1.post("/bonds/", createData)
        data1 = client1.get("/bonds/")
        print("\nClient 1 data:")
        print(data1.content)

        token2 = Token.objects.get(user__username='adversary')
        client2 = APIClient()
        client2.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
        data2 = client2.get("/bonds/")
        print("\nClient 2 data:")
        print(data2.content)
        assert (data1.status_code == 200 and data2.status_code == 200)

    def test_bond_creation(self):
        print("\n/////////////////////")
        print("TESTING BOND CREATION")
        print("/////////////////////\n")
        self.authoriseClient()
        createData = {'isin':'GB0000121104', 'size':200000, 'currency':'GBP', 'maturity':'2025-03-01', 'lei':'R0MUWSFPU8MPRO8K5P83'}
        resp = self.client.post("/bonds/", createData)
        assert resp.status_code == 201

    def test_bond_search(self):
        print("\n/////////////////////")
        print("TESTING BOND SEARCH")
        print("/////////////////////\n")
        self.authoriseClient()
        createData1 = {'isin':'GB0000121104', 'size':200000, 'currency':'GBP', 'maturity':'2025-03-01', 'lei':'5493000IBP32UQZ0KL24'}
        createData2 = {'isin':'FR0000121104', 'size':200000, 'currency':'EUR', 'maturity':'2025-03-01', 'lei':'R0MUWSFPU8MPRO8K5P83'}
        self.client.post("/bonds/", createData1)
        self.client.post("/bonds/", createData2)
        resp = self.client.get("/bonds/?legal_name=BNPPARIBAS")
        print(resp.content)
        assert resp.status_code == 200

    def test_bond_retrieval(self):
        print("\n/////////////////////")
        print("TESTING BOND RETRIEVAL")
        print("/////////////////////\n")
        self.authoriseClient()
        resp = self.client.get("/bonds/")
        print(resp.content)
        assert resp.status_code == 200

    def createTokens(self):
        users = User.objects.all()
        for user in users:
            token, created = Token.objects.get_or_create(user=user)

    def authoriseClient(self):
        token = Token.objects.get(user__username='origin')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
