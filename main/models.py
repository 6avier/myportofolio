import uuid
from django.contrib.auth.models import User
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    starred_by = models.ManyToManyField(User, related_name="starred_experiences", blank=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    institution = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.institution


class Project(models.Model):
    title = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    description = models.TextField()
    year = models.CharField(max_length=20)
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    starred_by = models.ManyToManyField(User, related_name="starred_projects", blank=True)

    def __str__(self):
        return self.title


class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('technical', 'Technical'),
        ('soft', 'Soft Skill'),
        ('tool', 'Tool'),
        ('language', 'Language'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, default='technical')
    proficiency = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name