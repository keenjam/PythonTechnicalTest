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
        self.createTokens()

    @classmethod
    def setUpTestData(cls):
        Bond.objects.create(isin="FR0000131104", size=100000000, currency="EUR", maturity="2025-02-28", lei="R0MUWSFPU8MPRO8K5P83")

    def test_unauthenticated_client(self):
        resp = self.client.get("/bonds/")
        assert resp.status_code == 401

    def test_bond_creation(self):
        self.authoriseClient()
        createData = {'isin':'GB0000121104', 'size':200000, 'currency':'GBP', 'maturity':'2025-03-01', 'lei':'R0MUWSFPU8MPRO8K5P83'}
        resp = self.client.post("/bonds/", createData)
        self.test_bond_retrieval()
        assert resp.status_code == 201

    def test_bond_search(self):
        self.authoriseClient()
        self.test_bond_creation()
        resp = self.client.get("/bonds/?legal_name=BNPPARIBAS")
        assert resp.status_code == 200

    def test_bond_retrieval(self):
        self.authoriseClient()
        resp = self.client.get("/bonds/")
        assert resp.status_code == 200

    def createTokens(self):
        users = User.objects.all()
        for user in users:
            token, created = Token.objects.get_or_create(user=user)

    def authoriseClient(self):
        token = Token.objects.get(user__username='origin')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
