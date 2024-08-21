from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("signup/", views.Register.as_view(), name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.Profile.as_view(), name="profile"),
    
    path("save_address/", views.SaveAddress.as_view(), name="save_address"),
    path("edit_address/<int:address_id>/", views.EditAddress.as_view(), name="edit_address"),
]