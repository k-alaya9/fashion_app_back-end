from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,ClothesViewSet,SavedViewSet
router=DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'clothes',ClothesViewSet)
router.register(r'saved',SavedViewSet,basename="saved")
urlpatterns = [
    path('',include(router.urls)),
]
