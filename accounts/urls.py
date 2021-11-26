from django.urls import path 
from .views import SignupView,LoginView,HomeView

urlpatterns = [
    path('signup/',SignupView,name='signup'),
    path('login/',LoginView,name='login'),
    path('pwdlesslogin/<str:token>/',HomeView,name='home'),

]