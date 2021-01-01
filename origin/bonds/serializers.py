from rest_framework.serializers import ModelSerializer
from bonds.models import Bond


class BondSerializer(ModelSerializer):
    class Meta:
        model = Bond
        fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']
