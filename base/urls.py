from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name="home"),
    path('loginf', loginf, name="login"),
    path('signupf', signupf, name="signup"),
    path('logoutf', logoutf, name="logout"),
    path('depositf', deposit, name="deposit"),
    path('postf/depositf', deposit, name="deposit"),
    path('postf/logoutf', logoutf, name="logout"),
    path('postf/<int:pk>', postv, name="postf"),
    path('delete/<int:pk>', deletev, name="deletev"),
    path('api/users', userapi.as_view()),
    path('api/posts', postsapi.as_view()),
]