from django.urls import path
from main.views import (
    show_main, show_experience, show_education, show_projects, show_skills,
    create_project, get_projects_json, delete_project,
    create_experience, update_experience, delete_experience, get_experience_json,
    register, login_user, logout_user, toggle_star, toggle_star_experience,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("projects/", show_projects, name="show_projects"),
    path("skills/", show_skills, name="show_skills"),
    path("projects/create/", create_project, name="create_project"),
    path("projects/json/", get_projects_json, name="get_projects_json"),
    path("projects/<int:id>/delete/", delete_project, name="delete_project"),
    path("experience/create/", create_experience, name="create_experience"),
    path("experience/<uuid:id>/update/", update_experience, name="update_experience"),
    path("experience/<uuid:id>/delete/", delete_experience, name="delete_experience"),
    path("experience/json/", get_experience_json, name="get_experience_json"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/<int:id>/star/", toggle_star, name="toggle_star"),
    path("experience/<uuid:id>/star/", toggle_star_experience, name="toggle_star_experience"),
]
