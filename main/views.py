from main.forms import ProjectForm
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
    json_response = get_projects_json(request)

    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Kemas Xavier",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)


def show_skills(request):
    context = {
        "name": "Kemas Xavier",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_projects')

    context = {"name": "Kemas Xavier", "form": form}
    return render(request, "project_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")