from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="blog-home"),
    path("about/", views.about, name="blog-about"),
    path("register/", views.register, name="register"),
    path("go_login/", views.go_login, name="go-login"),
    path("login", views.login),
    path("register_process", views.register_process),
    path("logout", views.logout, name="logout"),
    path("profile/<int:id>", views.profile, name="user-profile"),
    path("view_post/<int:id>", views.view_post),
    path("new_post/", views.new_post, name="new-post"),
    path("new_post_process/", views.new_post_process),
    path("update_user/<int:id>", views.update_user),
    path("update_user_process/<int:id>", views.update_user_process),
    path("update_post/<int:id>", views.update_post, name="update_post"),
    path("update_post_process/<int:id>", views.update_post_process),
    path("all_users", views.all_users, name="all-users"),
    path("oops", views.oops, name="oops"),
]