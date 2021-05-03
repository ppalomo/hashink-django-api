from django.contrib import admin
from .models import Signer, GroupSig, GroupSig_Signer, Request, Request_Signer, Category, Charity, Drop

admin.site.register(Category)
admin.site.register(Charity)
admin.site.register(Drop)
admin.site.register(GroupSig)
admin.site.register(GroupSig_Signer)
admin.site.register(Request)
admin.site.register(Request_Signer)
admin.site.register(Signer)
