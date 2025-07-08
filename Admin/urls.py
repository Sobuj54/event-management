from django.urls import path
from Admin.views import admin_dashboard

app_name="Admin"

urlpatterns = [
    path("home/", admin_dashboard , name="home"),

]
