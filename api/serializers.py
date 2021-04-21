from rest_framework import serializers
from api.models import Signer, GroupSig, Request


class SignerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'full_name', 'email', 'address', 'price',
                  'price_eth', 'response_time', 'avatar', 'autograph', 'active', 'created_at')


class SignerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        fields = ('full_name', 'address', 'price', 'response_time')


class GroupSigDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupSig
        fields = '__all__'


class GroupSigListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupSig
        fields = ('name', 'price', 'response_time')


class RequestDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = '__all__'


class RequestListSerializer(serializers.ModelSerializer):
    signers = SignerListSerializer(many=True)

    class Meta:
        model = Request
        fields = ('requester_address', 'name', 'price',
                  'response_time', 'state', 'groupsig', 'signer', 'signers')
