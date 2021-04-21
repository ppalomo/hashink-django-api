from rest_framework import serializers
from api.models import Signer


class SignerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'full_name', 'email', 'address', 'price',
                  'price_eth', 'response_time', 'avatar', 'autograph', 'active', 'created_at')


class SignerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        fields = ('full_name', 'email', 'address', 'price')
