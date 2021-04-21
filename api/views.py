from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from api.models import Signer
from .serializers import SignerListSerializer, SignerDetailSerializer


class SignerViewSet(viewsets.ModelViewSet):
    queryset = Signer.objects.all()
    serializer_class = SignerDetailSerializer
