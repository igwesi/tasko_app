from django.contrib import admin
from .models import Profile, Skill, SocialLink
from unfold.admin import ModelAdmin
from unfold.decorators import action
from django.db.models import QuerySet
from django.http import HttpRequest


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user',)
    filter_horizontal = ('skills',)

    fieldsets = (
        (None, {'fields': ('user', 'bio')}),
        ('Skills', {'fields': ('skills',)}),
    )
    save_as = True
    save_on_top = True
    list_select_related = True

    actions_list = ["add"]
    
    @action(description="Add New")
    def add(self, request: HttpRequest):
        pass

@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ('owner', 'github')
    search_fields = ('owner',)
    list_select_related = True

    fieldsets = (
        ("Profile Information", {'fields': ('owner',)}),
        ('Social Media Links', {'fields': ('facebook', 'github', 'instagram', 'linkedin', 'reddit', 'telegram', 'twitch', 'tiktok', 'twitter')}),
    )

    save_as = True
    save_on_top = True
    actions_list = ["add"]
    
    @action(description="Add New")
    def add(self, request: HttpRequest):
        pass

@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_select_related = True
    save_as = True
    save_on_top = True

    fieldsets = (
        ("Skill Information", {'fields': ('name',)}),
    )

    actions_list = ["add"]

    @action(description="Add New")
    def add(self, request: HttpRequest):
        pass