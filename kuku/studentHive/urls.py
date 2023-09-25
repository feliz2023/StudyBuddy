from django.urls import path
from . import views

urlpatterns = [
    path('loginP/', views.loginP, name="loginP"),
    path('logoutPage/', views.logoutUser, name="logoutPage"),
    path('registerPage/', views.registerUser, name="registerPage"),
    path('homePage/', views.home, name="homePage"),
    path('roomPage/<str:pk>/', views.room, name="roomPage"),
    path('st-profile/<str:pk>/', views.userProfile, name='st-profile'),

    path('create-roomPage/', views.createRoom, name="create-roomPage"),
    path('update-roomPage/<str:pk>/', views.updateRoom, name="update-roomPage"),
    path('delete-roomPage/<str:pk>/', views.deleteRoom, name="delete-roomPage"),
    path('delete-Ymessage/<str:pk>/', views.deleteMessage, name="delete-Ymessage"),
    path('update-st/', views.updateUser, name="update-st"),
    path('topicss/', views.topicsPages, name="topicss"),
    path('activityPage/', views.activityPage, name="activityPage"),

]
