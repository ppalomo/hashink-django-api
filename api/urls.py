from django.urls import include, path
from rest_framework import routers
from .views import SignerViewSet

router = routers.DefaultRouter()
router.register('signers', SignerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
