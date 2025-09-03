from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),

    # Search
    path("search/", views.search_page, name="search"),
    path("search/api/", views.search_api, name="search_api"),

    # Dashboard / Profile
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("user/update/", views.user_update, name="user_update"),
    path("user/<str:username>/", views.user_view, name="user-profile"),

    # Auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Ideas
    path("idea/create/", views.idea_create, name="idea_create"),
    path("idea/<slug:slug>/", views.idea_detail, name="idea-detail"),
    path("idea/<slug:slug>/edit/", views.idea_update, name="idea_update"),
    path("idea/<slug:slug>/delete/", views.idea_delete, name="idea_delete"),

    # Newsletter
    path("subscribe/", views.subscribe_newsletter, name="subscribe_newsletter"),
]
