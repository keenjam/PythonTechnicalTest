from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json, requests
from bonds.models import Bond
from bonds.serializers import BondSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class HelloWorld(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response("Hello World!")

class Bonds(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def getLegalName(self, lei):
        updatedUrl = 'https://leilookup.gleif.org/api/v2/leirecords?lei=' + str(lei)
        # take in and parse JSON from lei lookup api
        data = requests.get(updatedUrl).json()[0]

        legalName = data['Entity']['LegalName']['$']
        return legalName

    def get(self, request):
        print("\nRETRIEVING...\n")

        # find, if any, request parameters
        searchParam = request.GET.get('legal_name', '')

        bonds = Bond.objects.all()

        if(searchParam != ''):
            print("SEARCHING FOR: " + searchParam)
            bonds = Bond.objects.filter(legal_name = searchParam)

        serializer = BondSerializer(bonds, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        print("\nCREATING...\n")
        lei = request.data['lei']
        legalName = self.getLegalName(lei)
        legalName = legalName.replace(" ", "")

        request.data._mutable = True
        request.data['legal_name'] = legalName
        request.data._mutable = False

        serializer = BondSerializer(data=request.data)
        if(serializer.is_valid()):
            print("SAVING BOND DATA...\n")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
