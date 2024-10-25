from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from api.views import API

admin.site.site_header = "Tasko Admin"
admin.site.site_title = "Tasko Admin Portal"
admin.site.index_title = "Welcome to Tasko Portal"
admin.site.site_url = "/api"


# API endpoints
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/", include([
        path("", API.as_view(), name="api"),
        path("user/", include(("apps.accounts.api.urls", "user"), namespace="user")),
        path("todo/", include(("apps.todo.api.urls", "project"), namespace="todo")),
    ])),

    # schemas
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name='schema'), name="docs"),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]