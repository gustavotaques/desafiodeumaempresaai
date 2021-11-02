from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from music.views import MusicViewSet

router = routers.DefaultRouter()
router.register('music', MusicViewSet, basename='music')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
