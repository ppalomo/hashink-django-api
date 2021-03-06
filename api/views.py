import pytz
import datetime
from .utils import get_subgraph_endpoint
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from rest_framework import viewsets, mixins, permissions
from .permissions import IsAdminOrReadOnly, IsReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from api.models import Signer, GroupSig, GroupSig_Signer, Request, Category, Charity, Drop
from .serializers import SignerListSerializer, SignerDetailSerializer
from .serializers import GroupSigListSerializer, GroupSigListTreeSerializer, GroupSigDetailSerializer
from .serializers import RequestListSerializer, RequestDetailSerializer
from .serializers import CategoryTreeListSerializer, CategoryFlatListSerializer, CategorySignersListSerializer
from .serializers import SignerGroupsigGenericSerializer, AutographSerializer
from .serializers import ChairityListSerializer
from .serializers import DropListSerializer, DropDetailSerializer
from operator import itemgetter

# region Signer


class SignerViewSet(viewsets.ModelViewSet):
    queryset = Signer.objects.filter(active=True)
    permission_classes = [IsReadOnly, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return SignerListSerializer
        if self.action == 'retrieve':
            return SignerDetailSerializer
        return SignerDetailSerializer

    def destroy(self, request, *args, **kwargs):
        signer = self.get_object()
        signer.active = False
        signer.save()
        return Response(data='delete success')

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

    @action(methods=['post'], detail=True)
    def print(self, request, *args, **kwargs):
        signer = self.get_object()
        signer.number_of_prints += 1
        signer.save()
        return Response(data='Printed signer')


# endregion

# region GroupSig


class GroupSigViewSet(viewsets.ModelViewSet):
    queryset = GroupSig.objects.all()
    permission_classes = [IsReadOnly, ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GroupSigDetailSerializer
        return GroupSigDetailSerializer

    def list(self, request):
        queryset = GroupSig.objects.filter(active=True)
        serializer = GroupSigListTreeSerializer(queryset, many=True)
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
    queryset = Request.objects.filter(state=0)
    filter_class = RequestListFilter
    permission_classes = [IsReadOnly, ]

    def get_permissions(self):
        if self.action in ('mint',):
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [IsReadOnly, ]
        return super(self.__class__, self).get_permissions()

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

    def destroy(self, request, *args, **kwargs):
        request = self.get_object()
        # if datetime.datetime.now() >= pytz.UTC.localize(request.created_at.replace(tzinfo=pytz.UTC)) + datetime.timedelta(days=request.response_time):
        request.state = 2
        request.save()
        return Response(data='delete success')
        # else:
        # return Response(None)

    @action(methods=['post'], detail=True)
    def mint(self, request, *args, **kwargs):
        request = self.get_object()
        request.state = 1
        request.save()
        return Response(data='request minted')


# endregion

# region Category


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategoryFlatListSerializer
    permission_classes = [IsReadOnly, ]

    def retrieve(self, request, pk=None):
        queryset = Category.objects.get(pk=pk)
        serializer = CategorySignersListSerializer(queryset, many=False)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def tree(self, request):
        queryset = Category.objects.filter(
            parent_category=None).order_by('name')
        serializer = CategoryTreeListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path=r'(?P<category_id>\d+)/(?P<signer_id>\d+)')
    def add_to_signer(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['category_id'])
        signer = Signer.objects.get(pk=kwargs['signer_id'])
        signer.categories.add(category)
        return Response(data='Category added')

    @action(methods=['delete'], detail=False, url_path=r'delete_from_signer/(?P<category_id>\d+)/(?P<signer_id>\d+)')
    def delete_from_signer(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['category_id'])
        signer = Signer.objects.get(pk=kwargs['signer_id'])
        signer.categories.remove(category)
        return Response(data='Category deleted')

# endregion

# region Autograph


class AutographViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategoryFlatListSerializer

    def list(self, request):
        sample_transport = RequestsHTTPTransport(
            url=get_subgraph_endpoint(),
            verify=True,
            retries=3,
        )

        client = Client(
            transport=sample_transport
        )
        query = gql('''
            query {
                autographs(first: 20) {
                    id
                    owner
                    creators
                    imageURI
                    metadataURI
                }
            }
        ''')
        response = client.execute(query)
        serializer = AutographSerializer(response['autographs'], many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r'owner/(?P<owner>\w+)')
    def owner(self, request, *args, **kwargs):
        sample_transport = RequestsHTTPTransport(
            url=get_subgraph_endpoint(),
            verify=True,
            retries=3,
        )
        client = Client(transport=sample_transport)
        query_string = '''
            query {
                autographs(where:{%s}) {
                    id
                    owner
                    creators
                    imageURI
                    metadataURI
                }
            }''' % '''owner:"{}"'''.format(kwargs['owner'])
        query = gql(query_string)
        response = client.execute(query)
        serializer = AutographSerializer(response['autographs'], many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r'signer/(?P<signer>\w+)')
    def signer(self, request, *args, **kwargs):
        sample_transport = RequestsHTTPTransport(
            url=get_subgraph_endpoint(),
            verify=True,
            retries=3,
        )
        client = Client(transport=sample_transport)
        query_string = '''
            query {
                autographs(where:{%s}) {
                    id
                    owner
                    creators
                    imageURI
                    metadataURI
                }
            }''' % '''creators_contains:["{}"]'''.format(kwargs['signer'])
        query = gql(query_string)
        response = client.execute(query)
        serializer = AutographSerializer(response['autographs'], many=True)

        return Response(serializer.data)


# endregion

# region Charity

class CharityViewSet(viewsets.ModelViewSet):
    queryset = Charity.objects.all()
    serializer_class = ChairityListSerializer
    permission_classes = [IsReadOnly, ]

# endregion

# region Drop


class DropViewSet(viewsets.ModelViewSet):
    queryset = Drop.objects.all()
    permission_classes = [IsReadOnly, ]

    def get_permissions(self):
        if self.action in ('request',):
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [IsReadOnly, ]
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return DropListSerializer
        if self.action == 'retrieve':
            return DropDetailSerializer
        return DropDetailSerializer

    @action(methods=['post'], detail=True)
    def request(self, request, *args, **kwargs):
        drop = self.get_object()

        utc = pytz.UTC
        now = datetime.datetime.now().replace(tzinfo=utc)
        starts_at = drop.starts_at.replace(tzinfo=utc)
        ends_at = drop.ends_at.replace(tzinfo=utc)

        if now >= starts_at and now < ends_at and drop.num_requests < drop.max_requests:
            requester_address = request.data.get('requester_address', None)
            image = request.data.get('image', None)
            message = request.data.get('message', None)

            # Creating new drop request
            new_request = Request.objects.create(
                requester_address=requester_address,
                price=drop.price,
                response_time=2,
                signer=drop.signer,
                groupsig=None,
                image=image,
                message=message
            )
            new_request.signers.set([drop.signer])
            new_request.save()

            # Updating drop data
            drop.num_requests += 1
            drop.total_raised += drop.price
            drop.save()

            serializer = DropDetailSerializer(drop)
            return Response(serializer.data)

        else:
            return Response(data='The drop is closed')


# endregion
