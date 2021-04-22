from rest_framework import serializers
from api.models import Signer, GroupSig, GroupSig_Signer, Request, Request_Signer


class SignerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        fields = ('id', 'full_name', 'address', 'price_eth',
                  'response_time', 'avatar', 'autograph', 'active')


class SignerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        fields = ('first_name', 'last_name', 'full_name', 'email', 'address', 'price',
                  'price_eth', 'response_time', 'avatar', 'autograph', 'active', 'created_at')


class GroupSig_SignerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='signer.full_name')
    address = serializers.ReadOnlyField(source='signer.address')

    class Meta:
        model = GroupSig_Signer
        fields = ('id', 'full_name', 'address')


class GroupSigDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupSig
        fields = '__all__'


class GroupSigListSerializer(serializers.ModelSerializer):
    signers = serializers.SerializerMethodField('get_active_signers')

    def get_active_signers(self, groupsig):
        qs = GroupSig_Signer.objects.filter(
            groupsig=groupsig, active=True, signer__active=True)
        serializer = GroupSig_SignerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = GroupSig
        fields = ('name', 'price', 'response_time', 'avatar', 'signers')


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
    signers = serializers.SerializerMethodField('get_active_signers')

    def get_active_signers(self, request):
        qs = Request_Signer.objects.filter(signer__active=True)
        serializer = Request_SignerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Request
        fields = ('id', 'requester_address', 'name', 'price',
                  'response_time', 'state', 'signers')

# class RequestListSerializer(serializers.ModelSerializer):
#     signers = serializers.SerializerMethodField('get_active_signers')

#     def get_active_signers(self, request):
#         qs = Signer.objects.filter(active=True)
#         serializer = SignerListSerializer(instance=qs, many=True)
#         return serializer.data

#     class Meta:
#         model = Request
#         fields = ('id', 'requester_address', 'name', 'price',
#                   'response_time', 'state', 'signers')
