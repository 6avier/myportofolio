from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.html import strip_tags
from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "role", "description", "year", "github_url", "demo_url"]

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Project name cannot be empty or contain only HTML tags.")
        return title

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Title cannot be empty or contain only HTML tags.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Description cannot be empty or contain only HTML tags.")
        return description
