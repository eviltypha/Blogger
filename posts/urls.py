from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('content', views.content, name='content'),
    path('logout', views.logout, name='logout'),
    path('create', views.create, name='create'),
    path('search', views.search, name='search')
]
