from django.contrib import admin
from .models import Signer, GroupSig, Request

admin.site.register(Signer)
admin.site.register(GroupSig)
admin.site.register(Request)
