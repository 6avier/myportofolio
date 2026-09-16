from django.urls import path
from main.views import show_main, show_experience, show_education, show_projects, show_skills, create_project, get_projects_json, delete_project
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
]