from django.urls import include, path
from rest_framework import routers
from .views import SignerViewSet, GroupSigViewSet, RequestViewSet

router = routers.DefaultRouter()
router.register('signers', SignerViewSet)
router.register('groupsigs', GroupSigViewSet)
router.register('requests', RequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
