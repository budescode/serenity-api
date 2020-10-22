from django.contrib import admin
from .models import Beginners, Intermediate, Advance

admin.site.register(Beginners)
admin.site.register(Intermediate)
admin.site.register(Advance)