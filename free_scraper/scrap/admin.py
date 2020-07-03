from django.contrib import admin
from .models import MCandidate
from .models import MProject
from .models import MBids


admin.site.register(MCandidate)
admin.site.register(MProject)
admin.site.register(MBids)

# Register your models here.
