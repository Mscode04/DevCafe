from django.contrib import admin

# Register your models here.
from .models import UserProfile, LoginTable

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(LoginTable)


