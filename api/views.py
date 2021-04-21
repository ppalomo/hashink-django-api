from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from api.models import Signer, GroupSig, Request
from .serializers import SignerListSerializer, SignerDetailSerializer
from .serializers import GroupSigListSerializer, GroupSigDetailSerializer
from .serializers import RequestListSerializer, RequestDetailSerializer


class SignerViewSet(viewsets.ModelViewSet):
    queryset = Signer.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SignerListSerializer
        if self.action == 'retrieve':
            return SignerDetailSerializer
        return SignerDetailSerializer


class GroupSigViewSet(viewsets.ModelViewSet):
    queryset = GroupSig.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupSigListSerializer
        if self.action == 'retrieve':
            return GroupSigDetailSerializer
        return GroupSigDetailSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RequestListSerializer
        if self.action == 'retrieve':
            return RequestDetailSerializer
        return RequestDetailSerializer
