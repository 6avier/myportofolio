from main.forms import ProjectForm, ExperienceForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Experience, Education, Project, Skill
from main.permissions import can_edit
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
import datetime


def show_main(request):
    last_login = request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan")
    context = {
        "name": "Kemas Xavier",
        "npm": "2506656886",
        "study_program": "S1 Sistem Informasi",
        "bio": "hi im an information systems student at csui nice too meeeet ya.",
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Kemas Xavier",
        "can_edit": can_edit(request.user),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Kemas Xavier",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Kemas Xavier",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


def show_skills(request):
    context = {
        "name": "Kemas Xavier",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_projects')

    context = {"name": "Kemas Xavier", "form": form}
    return render(request, "project_form.html", context)

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse({"message": "Only the portfolio owner can add projects."}, status=403)

    form = ProjectForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {"message": "Invalid data.", "errors": form.errors.get_json_data()},
            status=400,
        )

    project = form.save()
    return JsonResponse({"message": "Project added successfully!", "id": project.id}, status=201)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_by = [user.username for user in project.starred_by.all()]
        data.append({
            "id": project.id,
            "title": project.title,
            "role": project.role,
            "description": project.description,
            "year": project.year,
            "github_url": project.github_url,
            "demo_url": project.demo_url,
            "starred_by": starred_by,
            "star_count": len(starred_by),
            "is_starred": request.user.is_authenticated and request.user.username in starred_by,
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def get_experience_json(request):
    experiences = Experience.objects.prefetch_related("starred_by").all()

    data = []
    for experience in experiences:
        starred_by = [user.username for user in experience.starred_by.all()]
        data.append({
            "id": str(experience.id),
            "title": experience.title,
            "description": experience.description,
            "category": experience.category,
            "category_display": experience.get_category_display(),
            "thumbnail": experience.thumbnail,
            "is_ongoing": experience.is_ongoing,
            "starred_by": starred_by,
            "star_count": len(starred_by),
            "is_starred": request.user.is_authenticated and request.user.username in starred_by,
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experience')

    context = {"name": "Kemas Xavier", "form": form, "is_update": False}
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def update_experience(request, id):
    if not can_edit(request.user):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experience')

    context = {"name": "Kemas Xavier", "form": form, "is_update": True}
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience entry deleted successfully!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {"name": "Kemas Xavier", "form": form}
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response

    context = {"name": "Kemas Xavier", "form": form}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


def _toggle_star(item, user):
    """Add the user's star if missing, otherwise remove it (max one star per user)."""
    if user in item.starred_by.all():
        item.starred_by.remove(user)
    else:
        item.starred_by.add(user)


@login_required(login_url="/login/")
def toggle_star(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == "POST":
        _toggle_star(project, request.user)

    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_star_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        _toggle_star(experience, request.user)

    return redirect("main:show_experience")
