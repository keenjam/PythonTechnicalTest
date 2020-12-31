# from rest_framework import serializers
# from bonds.models import Bond
#
# class BondSerializer(serializers.Serializer):
#     model = Bond
#
#     def create(self):
#         fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']
#
#     def show(self):
#         fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']
from rest_framework.serializers import ModelSerializer
from bonds.models import Bond


class BondSerializer(ModelSerializer):
    class Meta:
        model = Bond
        fields = [
            'isin',
            'size',
            'currency',
            'maturity',
            'lei',
            'legal_name'
        ]
# 
# class BondCreateSerializer(ModelSerializer):
#     class Meta:
#         model = Bond
#         fields = [
#             'isin',
#             'size',
#             'currency',
#             'maturity',
#             'lei',
#             'legal_name'
#         ]
