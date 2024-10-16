from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Tasko Admin"
admin.site.site_title = "Tasko Admin Portal"
admin.site.index_title = "Welcome to Tasko Portal"
admin.site.site_url = "/api"


urlpatterns = [
    path("api/", include("api.urls")),
    path("api/todo/", include("apps.todo.api.urls")),
    path("api/user/", include("apps.accounts.api.urls")),
    path('admin/', admin.site.urls),
]