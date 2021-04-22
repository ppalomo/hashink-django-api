from django.urls import include, path
from rest_framework import routers
from .views import SignerViewSet, GroupSigViewSet, RequestViewSet

router = routers.DefaultRouter()
router.register('signer', SignerViewSet)
router.register('groupsig', GroupSigViewSet)
router.register('request', RequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
