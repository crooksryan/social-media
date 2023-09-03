
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path('profile/<str:id>/', views.profile, name='profile'),
    path('list/<str:option>/<str:id>', views.listing, name='list'),
    path('likes', views.likes, name='likes'),
    path('edit', views.edit, name='edit')
]
