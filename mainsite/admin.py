from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import TrcTech, ForSystem


class TrcTechAdmin(admin.ModelAdmin):
    list_display = ("id", "news_source", "news_cate", "news_title", "news_date", "news_url")
    
admin.site.register(TrcTech, TrcTechAdmin)


class ForSystemAdmin(admin.ModelAdmin):
    list_display = ("check_time",)

admin.site.register(ForSystem, ForSystemAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "display_groups", "password", "is_staff", "is_active", "date_joined")

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = "Groups"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CustomGroupAdmin(GroupAdmin):
    list_display = ("name", "display_members")

    def display_members(self, obj):
        members = User.objects.filter(groups=obj)
        return ", ".join([member.username for member in members])

admin.site.unregister(Group)
admin.site.register(Group,CustomGroupAdmin)