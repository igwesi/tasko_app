from django.contrib import admin
from .models import Account
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(Group)


@admin.register(Account)
class AccountAdmin(ModelAdmin, UserAdmin):
    list_display    = ("email", "is_staff", "is_superuser")
    search_fields   = ("email",)
    list_filter     = ("is_staff", "is_admin", "is_superuser")
    
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("User Permissions", {"fields": ("is_staff","is_admin", "is_superuser")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "is_staff", "is_active", "is_superuser"),
            },
        ),
    )
    ordering = ("email",)
    
    filter_horizontal = ()
    save_on_top = True
    save_as     = True
    form        = UserChangeForm
    add_form    = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    