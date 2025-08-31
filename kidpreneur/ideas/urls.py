from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path('dashboard/user-update/', views.user_update, name='user_update'),
        
    path("search/", views.search_view, name="search"),

    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # Testing
    path("basetest", views.basetest_view, name="basetest"),

    # auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # idea CRUD
    # path("idea/", views.idea_list, name="idea_list"),
    path("idea/detail/<slug:slug>/", views.idea_detail, name="idea_detail"),
    path("idea/create/", views.idea_create, name="idea_create"),
    path("idea/update/<slug:slug>/", views.idea_update, name="idea_update"),
    path("idea/delete/<slug:slug>/", views.idea_delete, name="idea_delete"),
]
