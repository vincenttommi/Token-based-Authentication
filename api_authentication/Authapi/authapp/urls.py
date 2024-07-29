from django.urls import path
from . import views



urlpatterns= [
    path('login/',views.login),
    path('test/', views.TestView),
    path('signup/',views.signup),
    path('logout/', views.logout)
    
]