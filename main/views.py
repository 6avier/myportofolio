from django.shortcuts import render
from main.models import Experience


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