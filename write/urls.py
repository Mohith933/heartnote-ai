from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("aiwrite/", views.aiwrite, name="aiwrite"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("api/generate/", views.generate_text, name="generate_text"),
    path("api/dashboard/", views.generate_dashboard, name="generate_dashboard"),
    path("api/signup/", views.signup_api),
path("api/delete-account/", views.logout_and_delete),

]















