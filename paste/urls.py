from django.urls import include, path

from rest_framework.routers import DefaultRouter

from paste import views


router = DefaultRouter()
router.register('', views.SnippetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
