from django.urls import include, path
from rest_framework import routers
from .views import SignerViewSet, GroupSigViewSet, RequestViewSet, CategoryViewSet, CharityViewSet
from .views import AutographViewSet, DropViewSet

router = routers.DefaultRouter()
router.register('signer', SignerViewSet)
router.register('groupsig', GroupSigViewSet)
router.register('request', RequestViewSet)
router.register('category', CategoryViewSet)
router.register('autograph', AutographViewSet)
router.register('charity', CharityViewSet)
router.register('drop', DropViewSet)

urlpatterns = [
    path('', include(router.urls))
]
