from django.shortcuts import render
from main.models import Experience, Education, Project, Skill


def show_main(request):
    context = {
        "name": "Kemas Xavier",
        "npm": "2506656886",
        "study_program": "S1 Sistem Informasi",
        "bio": "hi im an information systems student at csui nice too meeeet ya.",
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Kemas Xavier",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Kemas Xavier",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def show_projects(request):
    context = {
        "name": "Kemas Xavier",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)


def show_skills(request):
    context = {
        "name": "Kemas Xavier",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)