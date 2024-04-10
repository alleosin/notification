from django.contrib import admin
from .models import Profile, Notification

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bill"]

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["sender", "addressee", "endowment", "text"]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
