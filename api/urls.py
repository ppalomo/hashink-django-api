from django.urls import include, path
from rest_framework import routers
from .views import SignerViewSet, GroupSigViewSet, RequestViewSet, CategoryViewSet
from .views import AutographViewSet

router = routers.DefaultRouter()
router.register('signer', SignerViewSet)
router.register('groupsig', GroupSigViewSet)
router.register('request', RequestViewSet)
router.register('category', CategoryViewSet)
router.register('autograph', AutographViewSet)

urlpatterns = [
    path('', include(router.urls))
]
