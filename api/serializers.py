from rest_framework import serializers
from api.models import Signer, GroupSig, GroupSig_Signer, Request, Request_Signer, Category

# region Signer


class SignerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signer
        fields = ('id', 'full_name', 'address', 'price_eth',
                  'response_time', 'avatar', 'autograph', 'active')


class SignerDetailSerializer(serializers.ModelSerializer):
    requests = serializers.SerializerMethodField('get_requests')

    def get_requests(self, signer):
        qs = Request_Signer.objects.filter(signer=signer)
        serializer = Request_SignerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Signer
        fields = ('first_name', 'last_name', 'full_name', 'email', 'address', 'price',
                  'price_eth', 'response_time', 'avatar', 'autograph', 'active', 'created_at', 'requests')


# endregion

# region GroupSig_Signer


class GroupSig_SignerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='signer.full_name')
    address = serializers.ReadOnlyField(source='signer.address')
    avatar = serializers.ImageField(source='signer.avatar')

    class Meta:
        model = GroupSig_Signer
        fields = ('id', 'full_name', 'address', 'avatar')

# endregion

# region GroupSig


class GroupSigDetailSerializer(serializers.ModelSerializer):
    signers = serializers.SerializerMethodField('get_signers')
    requests = serializers.SerializerMethodField('get_requests')

    def get_signers(self, groupsig):
        qs = GroupSig_Signer.objects.filter(
            groupsig=groupsig, active=True, signer__active=True)
        serializer = GroupSig_SignerSerializer(instance=qs, many=True)
        return serializer.data

    def get_requests(self, groupsig):
        qs = Request.objects.filter(
            groupsig=groupsig)
        serializer = RequestListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = GroupSig
        fields = ('id', 'name', 'price', 'response_time',
                  'avatar', 'signers', 'requests')


class GroupSigListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupSig
        fields = ('id', 'name', 'price_eth',
                  'response_time', 'avatar')


class GroupSigListTreeSerializer(serializers.ModelSerializer):
    signers = serializers.SerializerMethodField('get_signers')

    def get_signers(self, groupsig):
        qs = GroupSig_Signer.objects.filter(
            groupsig=groupsig, active=True, signer__active=True)
        serializer = GroupSig_SignerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = GroupSig
        fields = ('id', 'name', 'price_eth',
                  'response_time', 'avatar', 'signers')


# endregion

# region Request_Signer


class Request_SignerSerializer(serializers.ModelSerializer):
    request_id = serializers.ReadOnlyField(source='request.id')
    signer_id = serializers.ReadOnlyField(source='signer.id')
    name = serializers.ReadOnlyField(source='request.name')
    full_name = serializers.ReadOnlyField(source='signer.full_name')
    address = serializers.ReadOnlyField(source='signer.address')

    class Meta:
        model = Request_Signer
        fields = ('request_id', 'signer_id', 'name', 'full_name',
                  'address', 'signed_at', 'is_signed')

# endregion

# region Request


class RequestDetailSerializer(serializers.ModelSerializer):
    signers = Request_SignerSerializer(source='request_signer_set', many=True)

    class Meta:
        model = Request
        fields = ('id', 'requester_address', 'name', 'price',
                  'response_time', 'state', 'groupsig', 'signer', 'signers', 'created_at', 'updated_at')


class RequestListSerializer(serializers.ModelSerializer):
    signers = serializers.SerializerMethodField('get_signers')

    def get_signers(self, request):
        qs = Request_Signer.objects.filter(
            request=request, signer__active=True)
        serializer = Request_SignerSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Request
        fields = ('id', 'requester_address', 'name', 'price',
                  'response_time', 'state', 'signers')

# endregion

# region Category


class CategoryTreeListSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField('get_subcategories')

    def get_subcategories(self, category):
        qs = Category.objects.filter(
            parent_category=category)
        serializer = CategoryTreeListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories')


class CategoryFlatListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class CategorySignersListSerializer(serializers.ModelSerializer):
    signers = SignerListSerializer(many=True)
    groupsigs = GroupSigListSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'groupsigs', 'signers')

# endregion

# region Generics


class SignerGroupsigGenericSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price_eth = serializers.FloatField()
    response_time = serializers.IntegerField()
    avatar = serializers.ImageField()
    is_groupsig = serializers.BooleanField()

    categories = serializers.SerializerMethodField('get_categories')

    def get_categories(self, item):
        if not item['is_groupsig']:
            signer = Signer.objects.get(pk=item['id'])
            serializer = CategoryFlatListSerializer(
                instance=signer.categories.all(), many=True)
            return serializer.data
        elif item['is_groupsig']:
            groupsig = GroupSig.objects.get(pk=item['id'])
            serializer = CategoryFlatListSerializer(
                instance=groupsig.categories.all(), many=True)
            return serializer.data

# endregion
