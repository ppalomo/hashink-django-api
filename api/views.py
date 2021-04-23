from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from api.models import Signer, GroupSig, GroupSig_Signer, Request, Category
from .serializers import SignerListSerializer, SignerDetailSerializer
from .serializers import GroupSigListSerializer, GroupSigDetailSerializer
from .serializers import RequestListSerializer, RequestDetailSerializer
from .serializers import CategoryTreeListSerializer, CategoryFlatListSerializer, CategorySignersListSerializer
from .serializers import SignerGroupsigGenericSerializer
from operator import itemgetter

# region Signer


class SignerViewSet(viewsets.ModelViewSet):
    queryset = Signer.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SignerDetailSerializer
        return SignerDetailSerializer

    def list(self, request):
        queryset = Signer.objects.filter(active=True)
        serializer = SignerListSerializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def all(self, request, pk=None):
        signers = Signer.objects.filter(active=True)
        groupsigs = GroupSig.objects.filter(active=True)

        signers_data = [{'id': signer.id, 'name': signer.full_name, 'price_eth': signer.price_eth, 'response_time': signer.response_time, 'avatar': signer.avatar, 'is_groupsig': False, 'categories': signer.categories}
                        for signer in signers]

        groupsigs_data = [{'id': groupsig.id, 'name': groupsig.name, 'price_eth': groupsig.price_eth, 'response_time': groupsig.response_time, 'avatar': groupsig.avatar, 'is_groupsig': True, 'categories': None}
                          for groupsig in groupsigs]

        # Union and sorting
        data = sorted((signers_data + groupsigs_data), key=lambda o: o['name'])

        serializer = SignerGroupsigGenericSerializer(data, many=True)
        return Response(serializer.data)


# endregion

# region GroupSig


class GroupSigViewSet(viewsets.ModelViewSet):
    queryset = GroupSig.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GroupSigDetailSerializer
        return GroupSigDetailSerializer

    def list(self, request):
        queryset = GroupSig.objects.filter(active=True)
        serializer = GroupSigListSerializer(queryset, many=True)
        return Response(serializer.data)

# endregion

# region Request


class RequestListFilter(filters.FilterSet):

    class Meta:
        model = Request
        fields = {
            'requester_address': ['iexact']
        }


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestDetailSerializer
    queryset = Request.objects.all()
    # filterset_class = RequestListFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return RequestListSerializer
        if self.action == 'retrieve':
            return RequestDetailSerializer
        if self.action == 'create':
            return RequestDetailSerializer
        return RequestDetailSerializer

    def create(self, request, *args, **kwargs):
        requester_address = request.data.get('requester_address', None)
        signer_id = request.data.get('signer_id', None)
        groupsig_id = request.data.get('groupsig_id', None)

        if signer_id is not None:
            signer = Signer.objects.get(pk=signer_id)
            groupsig = None
            price = signer.price
            response_time = signer.response_time
            signers = [signer]
        elif groupsig_id is not None:
            groupsig = GroupSig.objects.get(pk=groupsig_id)
            signer = None
            price = groupsig.price
            response_time = groupsig.response_time
            groupsig_signers = GroupSig_Signer.objects.filter(
                groupsig_id=groupsig_id, active=True)
            signers = []
            for gs in groupsig_signers:
                s = Signer.objects.get(pk=gs.signer_id)
                if s.active:
                    signers.append(s)

        new_request = Request.objects.create(
            requester_address=requester_address,
            price=price,
            response_time=response_time,
            signer=signer,
            groupsig=groupsig
        )

        new_request.signers.set(signers)
        new_request.save()
        serializer = RequestDetailSerializer(new_request)
        return Response(serializer.data)

# endregion

# region Category


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategoryFlatListSerializer

    @action(methods=['get'], detail=False)
    def tree(self, request):
        queryset = Category.objects.filter(
            parent_category=None).order_by('name')
        serializer = CategoryTreeListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def signers(self, request, pk=None):
        queryset = Category.objects.get(pk=pk)
        serializer = CategorySignersListSerializer(queryset, many=False)
        return Response(serializer.data)

# endregion
