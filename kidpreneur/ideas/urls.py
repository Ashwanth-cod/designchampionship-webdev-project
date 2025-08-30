from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # idea CRUD
    path("idea/", views.idea_list, name="idea_list"),
    path("idea/detail/<slug:slug>/", views.idea_detail, name="idea_detail"),
    path("idea/create/", views.idea_create, name="idea_create"),
    path("idea/update/<slug:slug>/", views.idea_update, name="idea_update"),
    path("idea/delete/<slug:slug>/", views.idea_delete, name="idea_delete"),
]
