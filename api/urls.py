from django.urls import path
from .views import *

urlpatterns = [
    path('', baseAPi, name="apiHome"),
    path("api/user/create/", userCreation.as_view(), name="userCreation"),
    path("api/user/login/", LoginUser.as_view(), name="userLogin"),
]
