from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,ClothesViewSet,SavedViewSet,ExperimentViewSet,FeedBackViewSet,HistoryViewSet
router=DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'clothes',ClothesViewSet)
router.register(r'saved',SavedViewSet,basename="saved")
router.register(r'experiment',ExperimentViewSet)
router.register(r'feedback',FeedBackViewSet)
router.register(r'history',HistoryViewSet,basename='history')
urlpatterns = [
    path('',include(router.urls)),
]
