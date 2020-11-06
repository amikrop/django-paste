from django.urls import include, path


urlpatterns = [
    path('', include('paste.urls')),
]
