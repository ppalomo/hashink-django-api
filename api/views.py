from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from api.models import Signer, GroupSig, Request
from .serializers import SignerListSerializer, SignerDetailSerializer
from .serializers import GroupSigListSerializer, GroupSigDetailSerializer
from .serializers import RequestListSerializer, RequestDetailSerializer

# list() (GET /date-list/)
# create()(POST /date-list/)
# retrieve()(GET date-list/<id>/)
# update() (PUT /date-list/<id>/)
# partial_update() (PATCH, /date-list/<id>/
# destroy() (DELETE /date-list/<id>/)


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


class GroupSigViewSet(viewsets.ModelViewSet):
    queryset = GroupSig.objects.all()

    # def get_queryset(self):
    #     return GroupSig.objects.filter(active=True)

    def get_serializer_class(self):
        # if self.action == 'list':
        #     return GroupSigListSerializer
        if self.action == 'retrieve':
            return GroupSigDetailSerializer
        return GroupSigDetailSerializer

    def list(self, request):
        queryset = GroupSig.objects.filter(active=True)
        serializer = GroupSigListSerializer(queryset, many=True)
        return Response(serializer.data)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()  # .filter(signer__response_time=2)

    def get_serializer_class(self):
        if self.action == 'list':
            return RequestListSerializer
        if self.action == 'retrieve':
            return RequestDetailSerializer
        return RequestDetailSerializer

# class UserViewSet(viewsets.ViewSet):
#     """
#     Example empty viewset demonstrating the standard
#     actions that will be handled by a router class.

#     If you're using format suffixes, make sure to also include
#     the `format=None` keyword argument for each action.
#     """

#     def list(self, request):
#         pass

#     def create(self, request):
#         pass

#     def retrieve(self, request, pk=None):
#         pass

#     def update(self, request, pk=None):
#         pass

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         pass
