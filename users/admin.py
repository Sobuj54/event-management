from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields" : ("first_name", "last_name", "email", "phone_number", "profile_picture")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")})
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            "fields" : ("username", "email", "password1", "password2", "phone_number", "profile_picture")
        })
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username", )