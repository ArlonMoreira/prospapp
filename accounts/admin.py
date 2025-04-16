from django.contrib import admin
from .models import Users, VerificationCode

admin.site.register(Users)
admin.site.register(VerificationCode)

# Register your models here.
