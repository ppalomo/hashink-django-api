from django.contrib import admin
from .models import Signer, GroupSig, GroupSig_Signer, Request, Request_Signer

admin.site.register(Signer)
admin.site.register(GroupSig)
admin.site.register(GroupSig_Signer)
admin.site.register(Request)
admin.site.register(Request_Signer)
