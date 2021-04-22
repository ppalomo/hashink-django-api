from rest_framework import serializers
from api.models import Signer, GroupSig, Request, Request_Signer


class SignerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'full_name', 'email', 'address', 'price',
                  'price_eth', 'response_time', 'avatar', 'autograph', 'active', 'created_at')


class SignerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        fields = ('id', 'full_name', 'address', 'price', 'response_time')


class GroupSigDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupSig
        fields = '__all__'


class GroupSigListSerializer(serializers.ModelSerializer):
    signers = SignerListSerializer(many=True)

    class Meta:
        model = GroupSig
        fields = ('name', 'price', 'response_time', 'signers')


class Request_SignerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='signer.full_name')
    address = serializers.ReadOnlyField(source='signer.address')

    class Meta:
        model = Request_Signer
        fields = ('id', 'full_name', 'address', 'signed_at', 'is_signed')


class RequestDetailSerializer(serializers.ModelSerializer):
    signers = Request_SignerSerializer(source='request_signer_set', many=True)

    class Meta:
        model = Request
        fields = ('id', 'requester_address', 'name', 'price',
                  'response_time', 'state', 'groupsig', 'signer', 'signers', 'created_at', 'updated_at')


class RequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'requester_address', 'name', 'price',
                  'response_time', 'state', 'signers')
