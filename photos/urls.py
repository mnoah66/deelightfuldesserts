from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('cupcakes/', views.menu, name="cupcakes"),
    path('contact/', views.contact, name="contact"),
    path('success/', views.success, name="success"),
    path('order/', views.order, name='order'),

    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('gallery/', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('photo/<str:pk>/delete', views.deletePhoto, name='delete_photo'),
    path('add/', views.addPhoto, name='add'),
]
